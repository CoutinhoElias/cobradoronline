(function (namespace, $) {
	"use strict";

	var DemoCalendar = function () {
		// Create reference to this instance
		var o = this;
		// Initialize app when document is ready
		$(document).ready(function () {
			o.initialize();
		});

	};
	var p = DemoCalendar.prototype;

	// =========================================================================
	// INIT
	// =========================================================================

	p.initialize = function () {
		this._enableEvents();

		this._initEventslist();
		this._initCalendar();
		this._displayDate();
	};

	// =========================================================================
	// EVENTS
	// =========================================================================

	// events
	p._enableEvents = function () {
		var o = this;

		$('#calender-prev').on('click', function (e) {
			o._handleCalendarPrevClick(e);
		});
		$('#calender-next').on('click', function (e) {
			o._handleCalendarNextClick(e);
		});
		$('.nav-tabs li').on('show.bs.tab', function (e) {
			o._handleCalendarMode(e);
		});
	};

	// =========================================================================
	// CONTROLBAR
	// =========================================================================

	p._handleCalendarPrevClick = function (e) {
		$('#calendar').fullCalendar('prev');
		this._displayDate();
	};
	p._handleCalendarNextClick = function (e) {
		$('#calendar').fullCalendar('next');
		this._displayDate();
	};
	p._handleCalendarMode = function (e) {
		$('#calendar').fullCalendar('changeView', $(e.currentTarget).data('mode'));
	};

	p._displayDate = function () {
		var selectedDate = $('#calendar').fullCalendar('getDate');
		$('.selected-day').html(moment(selectedDate).format("dddd"));
		$('.selected-date').html(moment(selectedDate).format("DD MMMM YYYY"));
		$('.selected-year').html(moment(selectedDate).format("YYYY"));
	};

	// =========================================================================
	// TASKLIST
	// =========================================================================

	p._initEventslist = function () {
		if (!$.isFunction($.fn.draggable)) {
			return;
		}
		var o = this;

		$('.list-events li ').each(function () {
			// create an Event Object (http://arshaw.com/fullcalendar/docs/event_data/Event_Object/)
			// it doesn't need to have a start or end
			var eventObject = {
				title: $.trim($(this).text()), // use the element's text as the event title
				className: $.trim($(this).data('className'))
			};

			// store the Event Object in the DOM element so we can get to it later
			$(this).data('eventObject', eventObject);

			// make the event draggable using jQuery UI
			$(this).draggable({
				zIndex: 999,
				revert: true, // will cause the event to go back to its
				revertDuration: 0, //  original position after the drag
			});
		});
	};

	// =========================================================================
	// CALENDAR
	// =========================================================================

	p._initCalendar = function (e) {
		if (!$.isFunction($.fn.fullCalendar)) {
			return;
		}

		var date = new Date();
		var d = date.getDate();
		var m = date.getMonth();
		var y = date.getFullYear();

		$('#calendar').fullCalendar({
		    locale: 'pt-br',
			height: 700,
			header: false,
			editable: true,
			droppable: true,
			selectable: true,
			selectHelper: true,

            ignoreTimezone: false,
            monthNames: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            monthNamesShort: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
            dayNames: ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sabado'],
            dayNamesShort: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'],
            titleFormat: {
                month: 'MMMM yyyy',
                week: "d[ MMMM][ yyyy]{ - d MMMM yyyy}",
                day: 'dddd, d MMMM yyyy'
            },

            columnFormat: {
                month: 'ddd',
                week: 'ddd d',
                day: ''
            },

            axisFormat: 'H:mm',
            timeFormat: {
                '': 'H:mm',
                agenda: 'H:mm{ - H:mm}'
            },

            buttonText: {
                prev: "&nbsp;&#9668;&nbsp;",
                next: "&nbsp;&#9658;&nbsp;",
                prevYear: "&nbsp;&lt;&lt;&nbsp;",
                nextYear: "&nbsp;&gt;&gt;&nbsp;",
                today: "Hoje",
                month: "Mês",
                week: "Semana",
                day: "Dia"
            },



			drop: function (date, allDay) { // this function is called when something is dropped
				// retrieve the dropped element's stored Event Object
				var originalEventObject = $(this).data('eventObject');

				// we need to copy it, so that multiple events don't have a reference to the same object
				var copiedEventObject = $.extend({}, originalEventObject);

				// assign it the date that was reported
				copiedEventObject.start = date;
				copiedEventObject.allDay = allDay;
				copiedEventObject.className = originalEventObject.className;

				// render the event on the calendar
				// the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
				$('#calendar').fullCalendar('renderEvent', copiedEventObject, true);

				// is the "remove after drop" checkbox checked?
				if ($('#drop-remove').is(':checked')) {
					// if so, remove the element from the "Draggable Events" list
					$(this).remove();
				}
			},

            //LISTA DE EVENTOS
            events: '/api/bookings/',


            eventClick:  function(event, jsEvent, view) {
                $('#visualizar_agenda #title').text(event.title);
                $('#visualizar_agenda #start').text(event.start.format('DD/MM/YYYY HH:mm:ss'));
                $('#visualizar_agenda #end').text(event.end.format('DD/MM/YYYY HH:mm:ss'));
//                $('#visualizar_agenda').modal('show');
                return false;
            },

            select: function(start, end){
                //$('#novoEvento #id_start').val(moment(start).format('DD/MM/YYYY HH:mm:ss'));
                //$('#novoEvento #id_end').val(moment(end).format('DD/MM/YYYY HH:mm:ss'));

                var form = $(this);

                $.ajax({
                    url: 'bookings/agendamento/novo/',
                    data: form.serialize(),
                    type: form.attr('method'),
                    dataType: 'json',

                    beforeSend: function () {
                        //$("#novoEvento").dialog({ modal: true, title: event.title, width:500, height:651});
                    },
                    success: function (data) {
                        //console.log(data.html_form);
                        $("#novoEvento").html(data.html_form).dialog({ modal: true, title: event.title, width:500, height:651});

                        $('#multi-select').multiSelect({});
                        $('#datepicker').datepicker();
                        $('#select').select2({});

                        var saveForm = function (e) {
                          console.log(e)
                          e.preventDefault();
                          var form = $(this);
                          $.ajax({
                            url: form.attr("action"),
                            data: form.serialize(),
                            type: form.attr("method"),
                            dataType: 'json',
                            success: function (data) {
                            console.log('Sucesso')

                            }
                          });
                          return false;
                        };

                        // Create booking
                        $("#novoEvento").on("submit", ".js-book-create-form", saveForm);
                    }
                });
                return false;
            },



            eventDrop: function(event, delta) {
                $.ajax({
                        type: "PUT",
                        url: '/api/bookings/' + event.id +'/edit/',
                        data: {

                              //user: event.user,
                              title: event.title,
                              start: event.start.format('L'),
                              end: event.end.format('L'),
                              all_day: true,
                              color: event.color,
                              editable: event.editable
                        },
                    success: function(json) {
                        alert(event.title + " foi modificado para data " + event.start.format('L'));
                    }
                });
            },


            eventResize: function(event) {
                $.ajax({
                        type: "PUT",
                        url: '/api/bookings/' + event.id +'/edit/',
                        data: {

                              //user: event.user,
                              title: event.title,
                              start: event.start.format(),
                              end: event.end.format(),
                              all_day: true,
                              color: event.color,
                              editable: event.editable,
                        },
                    success: function(json) {
                        alert(event.title + " foi modificado para data " + event.start.format('L'));
                    }
                });

            },

//			eventRender: function (event, element) {
//				element.find('#date-title').html(element.find('span.fc-event-title').text());
//			}

//             eventRender: function(event, element) {
//                  $(element).popover({title: event.title, content: 'Inicia em: ' + event.start.format('DD/MM/YYYY HH:mm:ss') + ' termina em: ' + event.end.format('DD/MM/YYYY HH:mm:ss'), trigger : 'hover'});
//
//              }


            eventRender: function (event, element) {
                element.attr('href', 'javascript:void(0);');
                element.click(function() {
                    $("#startTime").html(moment(event.start).format('MMM Do h:mm A'));
                    $("#endTime").html(moment(event.end).format('MMM Do h:mm A'));
                    $("#eventInfo").html(event.description);
                    $("#eventLink").attr('href', event.url);
                    $("#eventContent").dialog({ modal: true, title: event.title, width:500, height:500});
                });
            }

		});


        var days = []

        $.get( "/api/bookings/feriado/", function( data ) {


            $.each(data, function(index, value){

                //alert(value.start.substr(0, 10))
                days.push(value.start.substr(0, 10))

            });


            $("td, th").each(function(){
                if(days.indexOf(this.dataset.date) >= 0){
                  $(this).css("background-color","red");
                }
            });

        });

	};

	// =========================================================================
	namespace.DemoCalendar = new DemoCalendar;
}(this.materialadmin, jQuery)); // pass in (namespace, jQuery):
