document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      plugins: [ 'interaction', 'dayGrid', 'timeGrid' ],
      defaultView: 'dayGridMonth',
      defaultDate: '2025-03-07',
      editable: true,
      selectable: true,
      selectMirror: true,
      header: {
        left: 'prev,today,next',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
      },
      events: [
        {
            title: "Blood test - Dr. chirag_12 (In-person)",
            start: "2025-03-28T13:54:49"
        },
        {
            title: "General Checkup - Dr. Smith (Virtual Consultation)",
            start: "2025-04-05T09:30:00",
            end: "2025-04-05T10:00:00"
        },
        {
            title: "Dental Cleaning - Dr. Brown (In-person)",
            start: "2025-04-10T14:00:00"
        },
        {
            title: "Eye Examination - Dr. Patel",
            start: "2025-04-15T11:00:00",
            end: "2025-04-15T11:30:00"
        },
        {
            title: "Annual Health Checkup - Dr. Williams",
            start: "2025-04-20T08:00:00"
        }
    ]
    
    });
    calendar.render();
  });