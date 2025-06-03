Handlebars.registerHelper('aimd-target', function (target) {
    if (target === undefined || target === null || target.length === 0) {
        return '';
    }
    const elements = new Set();
    for (const obj of target) {
      if (obj.hasOwnProperty('element')) {
        elements.add(obj.element);
      }
    }
    return Array.from(elements).join('');
});
Handlebars.registerHelper('split', function (string, separator, index) {
    try {
        return string.split(separator)[index].trim();
    } catch (e) {
        return '';
    }
});
