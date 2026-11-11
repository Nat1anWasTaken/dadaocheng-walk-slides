/**
 * Slide changes run through the View Transitions API (styles in styles/motion.css).
 *
 * Slidev's own `transition: view-transition` swaps the slideshow between a <div> and a
 * <TransitionGroup> whenever a click follows a slide change, which remounts every slide
 * and kills click animations. So the theme's default `transition` is a CSS-less no-op
 * (package.json; it swaps slides synchronously, so the old one is already hidden when
 * the new state is captured) and the view transition starts here instead.
 *
 * Before each slide change the hook tags <html> with
 *   data-deck-nav="forward | backward"
 *   data-deck-motion="<frontmatter `motion`>"
 * Like Slidev's `transition`, a slide's `motion` applies when leaving it forward and
 * when coming back to it.
 */
import { defineAppSetup } from '@slidev/types'
import { nextTick } from 'vue'
import { slides } from '#slidev/slides'

const getSlide = (no: unknown) => slides.value.find(s => s.no === Number(no))

export default defineAppSetup(({ router }) => {
  if (typeof document === 'undefined')
    return
  const root = document.documentElement
  let finishUpdate: (() => void) | undefined

  router.beforeResolve((to, from) => {
    if ('print' in to.query || to.path.includes('/export') || to.path.includes('/print'))
      return
    const fromSlide = getSlide(from.params.no)
    const toSlide = getSlide(to.params.no)
    if (!fromSlide || !toSlide || fromSlide.no === toSlide.no)
      return

    const forward = toSlide.no > fromSlide.no
    const motion = (forward ? fromSlide : toSlide).meta.slide?.frontmatter.motion
    // Tagging <html> switches entrance animations on, so it waits until the old state is
    // captured: otherwise they would restart on the slide being left.
    const tag = () => {
      root.dataset.deckNav = forward ? 'forward' : 'backward'
      root.dataset.deckMotion = typeof motion === 'string' ? motion : 'default'
    }

    if (!document.startViewTransition || document.visibilityState !== 'visible') {
      tag()
      return
    }

    // Resolve once the old state is captured; the route then changes inside the update callback.
    return new Promise<void>((resolve) => {
      finishUpdate?.()
      document.startViewTransition(() => new Promise<void>((done) => {
        tag()
        finishUpdate = done
        resolve()
      }))
    })
  })

  // Also runs for aborted navigations, so a transition never waits on a route that never came.
  router.afterEach(async () => {
    const done = finishUpdate
    if (!done)
      return
    finishUpdate = undefined
    await nextTick()
    done()
  })
})
