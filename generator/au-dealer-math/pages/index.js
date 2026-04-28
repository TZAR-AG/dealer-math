const cover = require('./01-cover');
const intro = require('./02-intro');
const line1 = require('./03-line-1');
const line2 = require('./04-line-2');
const line3 = require('./05-line-3');
const line4 = require('./06-line-4');
const line5 = require('./07-line-5');
const line6 = require('./08-line-6');
const line7 = require('./09-line-7');
const cta = require('./10-cta');

function renderAllPages(theme) {
  return [
    cover.render(theme),
    intro.render(theme),
    line1.render(theme),
    line2.render(theme),
    line3.render(theme),
    line4.render(theme),
    line5.render(theme),
    line6.render(theme),
    line7.render(theme),
    cta.render(theme),
  ].join('\n');
}

module.exports = { renderAllPages };
