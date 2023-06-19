/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    // TODO うまく動かないため無効にする
    typedRoutes: false,
    serverActions: true,
  },
  output: 'standalone',
};

module.exports = nextConfig;
