import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,

  // The React Compiler handles memoisation. Do not add useMemo or useCallback
  // for performance reasons; hand-rolled memoisation can defeat it.
  reactCompiler: true,

  // Partial pre-rendering. The static shell streams instantly and dynamic
  // holes fill in behind Suspense, so every Suspense boundary needs a real
  // skeleton at the final dimensions.
  cacheComponents: true,
  partialPrefetching: true,

  turbopack: {
    rules: {
      '*.css': {
        loaders: ['@tailwindcss/turbopack'],
        as: '*.css',
      },
    },
  },
};

export default nextConfig;
