/** @type {import('next').NextConfig} */
const nextConfig = {
  basePath: '/news-intel',
  output: 'export',
  trailingSlash: true,
  images: { unoptimized: true },
  env: {
    NEXT_PUBLIC_BASE_PATH: '/news-intel',
    NEXT_PUBLIC_SITE_URL: 'https://cearl.cc',
  },
}

module.exports = nextConfig
