const CLOUDINARY_REGEX = /^(https?:\/\/res\.cloudinary\.com\/[\w-]+\/image\/upload)\/(.*)$/

export function cloudinaryUrl(url: string, transforms = 'f_auto,q_auto,c_fill,w_400'): string {
  const match = url.match(CLOUDINARY_REGEX)
  if (!match) return url
  return `${match[1]}/${transforms}/${match[2]}`
}
