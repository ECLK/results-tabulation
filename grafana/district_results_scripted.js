'use strict';

// accessible variables in this scope
var window, document, ARGS, $, jQuery, moment, kbn;


var rows = 1;
var seriesName = 'argName';
var user = window.grafanaBootData.user.login


return function (callback) {

    var rows = 1;
    var seriesName = 'argName';

    $.ajax({
        method: 'GET',
        async: false,
        global: false,
        url: '/district_result_status.json',
        dataType: "json",
    }).done(function (result) {
            var district = null
            if (!_.isUndefined(ARGS.district)) {
                switch (user){
                    case 'colombo':
                        district = '01 - Colombo';
                        break;
                    case 'gompaha':
                        district = '02 - Gampaha';
                        break;
                    case 'kalutara':
                        district = '03 - Kalutara';
                        break;
                    case 'kandy':
                        district = '04 - Kandy';
                        break;
                    case 'matale':
                        district = '05 - Matale';
                        break;
                    case 'nuwaraeliya':
                        district = '06 - Nuwara Eliya';
                        break;
                    case 'gall':
                        district = '07 - Gall';
                        break;
                    case 'matara':
                        district = '08 - Matara';
                        break;
                    case 'hambantota':
                        district = '09 - Hambantota';
                        break;
                    case 'jaffna':
                        district = '10 - Jaffna';
                        break;
                    case 'vanni':
                        district = '11 - Vanni';
                        break;
                    case 'batticaloa':
                        district = '12 - Batticaloa';
                        break;
                    case 'digamdulla':
                        district = '13 - Digamdulla';
                        break;
                    case 'trincomalee':
                        district = '14 - Trincomalee';
                        break;
                    case 'krunegala':
                        district = '15 - Krunegala';
                        break;
                    case 'puttalam':
                        district = '16 - Puttalam';
                        break;
                    case 'anuradhapura':
                        district = '17 - Anuradhapura';
                        break;
                    case 'polannaruwa':
                        district = '18 - Polannaruwa';
                        break;
                    case 'badulla':
                        district = '19 - Badulla';
                        break;
                    case 'monaragala':
                        district = '20 - monaragala';
                        break;
                    case 'ratnapura':
                        district = '21 - Ratnapura';
                        break;
                    case 'kegalle':
                        district = '22 - Kegalle';
                        break;
                }
               
            }

            var code = {
                value: district,
                text: district,
                selected: true
            }
            var scynDashboard = result.dashboard;
            scynDashboard.templating.list[1].options.push(code)
            scynDashboard.templating.list[1].current = code;


            // when dashboard is composed call the callback
            // function and pass the dashboard
            callback(scynDashboard);

        });
}
