// Your Client ID can be retrieved from your project in the Google
      // Developer Console, https://console.developers.google.com
      var CLIENT_ID = '';

      var SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"];

      /**
       * Check if current user has authorized this application.
       */
      function checkAuth() {
        gapi.auth.authorize(
          {
            'client_id': CLIENT_ID,
            'scope': SCOPES,
            'immediate': true
          }, handleAuthResult);
      }

      /**
       * Handle response from authorization server.
       *
       * @param {Object} authResult Authorization result.
       */
      function handleAuthResult(authResult) {
        var authorizeDiv = document.getElementById('authorize-div');
        var outputDiv = document.getElementById('output');
        if (authResult && !authResult.error) {
          // Hide auth UI, then load client library.
          authorizeDiv.style.display = 'none';
          output.style.display = 'block';
          loadCalendarApi();
        } else {
          // Show auth UI, allowing the user to initiate authorization by
          // clicking authorize button.
          authorizeDiv.style.display = 'inline';
          output.style.display = 'none';
        }
      }

      /**
       * Initiate auth flow in response to user clicking authorize button.
       *
       * @param {Event} event Button click event.
       */
      function handleAuthClick(event) {
        gapi.auth.authorize(
          {client_id: CLIENT_ID, scope: SCOPES, immediate: false},
          handleAuthResult);
        return false;
      }

      /**
       * Load Google Calendar client library. List upcoming events
       * once client library is loaded.
       */
      function loadCalendarApi() {
        gapi.client.load('calendar', 'v3', listUpcomingEvents);
      }

      /**
       * Print the summary and start datetime/date of the next ten events in
       * the authorized user's calendar. If no events are found an
       * appropriate message is printed.
       */
      function listUpcomingEvents() {
        var request = gapi.client.calendar.events.list({
          'calendarId': 'primary',
          'timeMin': (new Date()).toISOString(),
          'showDeleted': false,
          'singleEvents': true,
          'maxResults': 10,
          'orderBy': 'startTime'
        });

        request.execute(function(resp) {
          var events = resp.items;
          var div = document.getElementById('output');
          var weekday = new Array(7);
          weekday[0]=  "Sun";
          weekday[1] = "Mon";
          weekday[2] = "Tue";
          weekday[3] = "Wed";
          weekday[4] = "Thu";
          weekday[5] = "Fri";
          weekday[6] = "Sat";
          // appendPre('Upcoming events:');

          if (events.length > 0) {
            for (i = 0; i < events.length; i++) {
              var event = events[i];
              var beg = event.start.dateTime;
              var end = event.end.dateTime;
              if (!beg) {
                beg = event.start.date;
              }
              if (!end) {
              	end = event.end.date;
              }
              var newEvent = document.createElement('div');
              var divIdName = 'event'+i;
              newEvent.setAttribute('id', divIdName);
              var beg_date = new Date(beg);
              var end_date = new Date(end);
              var date = event.summary +'-'+ weekday[beg_date.getDay()] + '-' + beg_date.getTime()+'-' + beg_date.getTimezoneOffset() +'-'+ end_date.getTime()+'-'+end_date.getTimezoneOffset();
              var display = weekday[beg_date.getDay()] +'. '+beg_date.toLocaleTimeString() +'-'+end_date.toLocaleTimeString();
              newEvent.innerHTML = event.summary + ' (' + display + ')' + ' <a id=\"add\" href=\"add/'+date+'/\">Save</a>';
              div.appendChild(newEvent);
              // appendPre(event.summary + ' (' + end_date.toLocaleString() + ')');
            }
          } else {
            // appendPre('No upcoming events found.');
          }

        });
      }

      /**
       * Append a pre element to the body containing the given message
       * as its text node.
       *
       * @param {string} message Text to be placed in pre element.
       */
      function appendPre(message) {
        var pre = document.getElementById('output');
        var textContent = document.createTextNode(message + '\n');
        pre.appendChild(textContent);
      }