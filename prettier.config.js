module.exports = {
  singleQuote: true,
  plugins: [
    require('prettier-plugin-tailwindcss'),
    require('prettier-plugin-organize-imports'),
  ],
  organizeImportsSkipDestructiveCodeActions: true,
};
