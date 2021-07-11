$("#top_query_counter").text($("#real_query_counter").data("counter"));
$.fn.datetimepicker.Constructor.Default = $.extend({}, $.fn.datetimepicker.Constructor.Default, {
    icons: {
        time: 'far fa-clock',
        date: 'far fa-calendar',
        up: 'fas fa-arrow-up',
        down: 'fas fa-arrow-down',
        previous: 'fas fa-chevron-left',
        next: 'fas fa-chevron-right',
        today: 'far fa-calendar-check-o',
        clear: 'far fa-trash',
        close: 'far fa-times'
    }
});
const pickerConfigs = {
    format: 'DD.MM.YYYY HH:mm',
    locale: 'uk',

};
let fromDate = null,
    toDate;
$(function () {
    $('#from_date').datetimepicker(Object.assign({
        defaultDate: moment({
            day: 1,
            month: 0,
            year: 2018,
            hour: 9
        }),
    }, pickerConfigs));
    $('#to_date').datetimepicker(Object.assign({
        useCurrent: false,
        defaultDate: moment({
            day: 1,
            month: 0,
            year: 2018,
            hour: 10
        }),
    }, pickerConfigs));
    $("#from_date").on("change.datetimepicker", function (e) {
        $('#to_date').datetimepicker('minDate', e.date);
    });
    $("#to_date").on("change.datetimepicker", function (e) {
        $('#from_date').datetimepicker('maxDate', e.date);
    });
});
$("#report_form").submit(function (event) {
    event.preventDefault();
    let serializedData = $(this).serialize();
    $.ajax({
        url: location.origin + location.pathname,
        data: serializedData,
        type: "GET",
        success: function (data) {
            let orders = $(data).filter("#orders").html();
            $("#orders").html(orders);
            window.history.pushState({"html": data.html, "pageTitle": data.pageTitle}, "", "?" + serializedData)
        }
    })

})