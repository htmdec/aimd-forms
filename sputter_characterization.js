const elements = ['Li', 'Be', 'Na', 'Mg', 'Al', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi'];

window.JSONEditor.defaults.callbacks.autocomplete = {
    'search_deposition': function (editor, input) {
        if (input.length < 2) {
            return [];
        }

        return restRequest({
            url: 'deposition',
            method: 'GET',
            data: {
                q: input,
                limit: 10
            }
        })
    },
    'render_deposition': function (editor, result, props) {
        try {
          const localId = result.metadata.alternateIdentifiers.find(
              (id) => id.alternateIdentifierType.toLowerCase() === 'local'
          );
          return `<li ${props}> ${result.igsn} (localId: ${localId.alternateIdentifier})</li>`;
        } catch (e) {
          return `<li ${props}> ${result.igsn} (title: ${result.metadata.titles[0]['title']})</li>`;
        }
    },
    'get_deposition_value': function (editor, result) {
        return result.igsn;
    },
    'search_element': function (editor, input) {
        const foo = elements
            .filter((el) => el.toLowerCase().startsWith(input.toLowerCase()))
            .map((el) => (el));
              ///{ label: el, value: el }));
        console.log(foo);
        return foo;
    }  
};
Handlebars.registerHelper('delta', function (a, b) {
  console.log(a, b);
  if (a === undefined || a === null ) {
    return -1;
  }
  if (b === undefined || b === null || b === 0) {
    return -1;
  }
  return Math.round((a - b) / a * 100);
});
Handlebars.registerHelper('FtoC', function (a, b) { 
  console.log(a, b);
  if (a === undefined || a === null ) {
    return -1;
  }
  if (b === undefined || b === null || b === 0) {
    return -1;
  }

  return Math.round((a - 32) * 5 / 9 * 100) / 100;
});
