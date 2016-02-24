'use strict';

var charts = [
    {
        'title': 'First',
        'signals': [1, 321]
    },
    {
        'title': 'Second',
        'signals': [1, 2, 3]
    },
    {
        'title': 'Third',
        'signals': [1, 3, 5, 7]
    }
];

// get unique signals values
var unique = charts.reduce(function (previousValue, currentValue) {
    return previousValue.concat(
        currentValue.signals.filter(function (item) {
            return previousValue.indexOf(item) < 0;
        })
    );
}, []);

// optional: sort numerically
unique.sort(function (a, b) {
    return a - b;
});

console.log(unique); // [ 1, 2, 3, 5, 7, 321 ]
