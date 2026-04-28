// AU Dealer Math single brand theme
const themes = {
  'au-dealer-math': {
    name: 'AU Dealer Math',
    bg: '#F5EFE6',          // cream
    heading: '#2B2B2B',     // charcoal
    body: '#4A4340',        // charcoal-soft
    accent: '#D17A3D',      // outback orange
    secondary: '#4A4340',
    grid: '#E0E0E0',
  },
};

function themeToCssVars(theme) {
  return `
    --bg: ${theme.bg};
    --heading: ${theme.heading};
    --body: ${theme.body};
    --accent: ${theme.accent};
    --secondary: ${theme.secondary};
    --grid: ${theme.grid};
  `;
}

module.exports = { themes, themeToCssVars };
