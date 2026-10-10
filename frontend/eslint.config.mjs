import { defineConfig, globalIgnores } from 'eslint/config';
import nextVitals from 'eslint-config-next/core-web-vitals';
import nextTs from 'eslint-config-next/typescript';
import jsxA11y from 'eslint-plugin-jsx-a11y';

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  {
    rules: {
      // Accessibility is a build failure, not a review comment. The rules are
      // spread rather than extending `jsxA11y.flatConfigs.strict` directly,
      // because eslint-config-next already registers the plugin and a flat
      // config cannot redefine one.
      ...jsxA11y.flatConfigs.strict.rules,
      // Product photography is the largest thing on any page. next/image is
      // not optional.
      '@next/next/no-img-element': 'error',
    },
  },
  globalIgnores(['.next/**', 'out/**', 'build/**', 'next-env.d.ts']),
]);

export default eslintConfig;
