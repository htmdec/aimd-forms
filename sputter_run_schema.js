Handlebars.registerHelper('multiply', function (a, b) { return a * b; });
Handlebars.registerHelper('divide', function (a, b) { 
  if (a === undefined || a === null ) {
    return -1;
  }
  if (b === undefined || b === null || b === 0) {
    return -1;
  }
  return a / b;
});
