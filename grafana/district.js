'use strict';

// accessible variables in this scope
var window, document, ARGS, $, jQuery, moment, kbn;

// Setup some variables
var dashboard;

// All url parameters are available via the ARGS object
var ARGS;

// Initialize a skeleton with nothing but a rows array and service object
dashboard = {
    rows: [],
};



// Set default time
// time can be overridden in the url using from/to parameters, but this is
// handled automatically in grafana core during dashboard initialization
dashboard.time = {
    from: "now-6h",
    to: "now"
};

var rows = 1;
var seriesName = 'argName';
var user = window.grafanaBootData.user.login


return function (callback) {

    // Setup some variables
    var dashboard;

    // Initialize a skeleton with nothing but a rows array and service object
    dashboard = {
        rows: [],
        services: {}
    };

    // Set a title
    // dashboard.title = 'District Dashbord';

    // Set default time
    // time can be overridden in the url using from/to parameters, but this is
    // handled automatically in grafana core during dashboard initialization
    dashboard.time = {
        from: "now-6h",
        to: "now"
    };

    var rows = 1;
    var seriesName = 'argName';

    $.ajax({
        method: 'GET',
        url: '/api/dashboards/uid/6CQ3Xj0Wk'
    })
        .done(function (result) {
            debugger;
            var district = null
                switch (user){
                    case 'colombo-ro':
                        district = '01 - Colombo';
                        break;
                    case 'gampaha-ro':
                        district = '02 - Gampaha';
                        break;
                    case 'kalutara-ro':
                        district = '03 - Kalutara';
                        break;
                    case 'kandy-ro':
                        district = '04 - Kandy';
                        break;
                    case 'matale-ro':
                        district = '05 - Matale';
                        break;
                    case 'nuwaraeliya-ro':
                        district = '06 - Nuwara Eliya';
                        break;
                    case 'galle-ro':
                        district = '07 - Galle';
                        break;
                    case 'matara-ro':
                        district = '08 - Matara';
                        break;
                    case 'hambantota-ro':
                        district = '09 - Hambantota';
                        break;
                    case 'jaffna-ro':
                        district = '10 - Jaffna';
                        break;
                    case 'vanni-ro':
                        district = '11 - Vanni';
                        break;
                    case 'batticaloa-ro':
                        district = '12 - Batticaloa';
                        break;
                    case 'digamdulla-ro':
                        district = '13 - Digamdulla';
                        break;
                    case 'trincomalee-ro':
                        district = '14 - Trincomalee';
                        break;
                    case 'krunegala-ro':
                        district = '15 - Krunegala';
                        break;
                    case 'puttalam-ro':
                        district = '16 - Puttalam';
                        break;
                    case 'anuradhapura-ro':
                        district = '17 - Anuradhapura';
                        break;
                    case 'polannaruwa-ro':
                        district = '18 - Polannaruwa';
                        break;
                    case 'badulla-ro':
                        district = '19 - Badulla';
                        break;
                    case 'monaragala-ro':
                        district = '20 - monaragala';
                        break;
                    case 'ratnapura-ro':
                        district = '21 - Ratnapura';
                        break;
                    case 'kegalle-ro':
                        district = '22 - Kegalle';
                        break;
                }

            var code = {
                value: district,
                text: district,
                selected: true
            }
            var scynDashboard = result.dashboard;
            scynDashboard.templating.list[2].options.push(code)
            scynDashboard.templating.list[2].current = code;


            // when dashboard is composed call the callback
            // function and pass the dashboard
            callback(scynDashboard);

        });
}
1
Downloading1
