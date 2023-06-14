module.exports = {
  singleQuote: true,
  plugins: [
    require('prettier-plugin-organize-imports'),
    require('prettier-plugin-tailwindcss'),
  ],
  pluginSearchDirs: false,
  organizeImportsSkipDestructiveCodeActions: true,
};
