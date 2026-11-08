import type { CSSProperties } from 'vue'

export function resolveAssetUrl(url: string) {
  if (url.startsWith('/'))
    return import.meta.env.BASE_URL + url.slice(1)
  return url
}

export function handleBackground(background?: string, dim = true, backgroundSize = 'cover'): CSSProperties {
  if (!background)
    return {}

  const isColor = ['#', 'rgb', 'hsl', 'var('].some(prefix => background.startsWith(prefix))

  if (isColor) {
    return {
      background,
      color: 'white',
    }
  }

  return {
    backgroundImage: dim
      ? `linear-gradient(120deg, rgba(24, 90, 188, 0.88), rgba(32, 33, 36, 0.72)), url("${resolveAssetUrl(background)}")`
      : `url("${resolveAssetUrl(background)}")`,
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    backgroundSize,
    color: dim ? 'white' : undefined,
  }
}

/**
 * True when a slot renders something visible (not just comments / whitespace).
 * Slidev always passes a default slot to layouts, even for an empty slide body.
 */
export function hasSlotContent(slot?: (...args: any[]) => any[]): boolean {
  if (!slot)
    return false
  const visible = (nodes: any[]): boolean => nodes.some((n) => {
    if (n == null || typeof n === 'boolean')
      return false
    if (typeof n === 'string')
      return n.trim().length > 0
    const type = typeof n.type === 'symbol' ? String(n.type) : ''
    if (type.includes('Comment'))
      return false
    if (type.includes('Text'))
      return typeof n.children === 'string' && n.children.trim().length > 0
    if (type.includes('Fragment'))
      return Array.isArray(n.children) && visible(n.children)
    return true
  })
  return visible(slot() ?? [])
}

/** One photo in a PhotoMosaic / mosaic layout */
export interface MosaicPhoto {
  src: string
  /** Tiny chip, e.g. "03 永樂市場" or "苦茶" */
  label?: string
  stop?: string | number
  /** object-position focal point, e.g. "50% 30%" */
  position?: string
  /** Aspect ratio (w/h) if you want to skip auto-detection: 0.75, "3/4", "portrait", "landscape" */
  ratio?: number | string
}
