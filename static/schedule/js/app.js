// CSRF対策
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"
document.addEventListener('DOMContentLoaded', function () {

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',

        locale: 'ja',

        timeZone: 'Asia/Tokyo',

        businessHours: true,

        headerToolbar: {
            left: 'prev',
            center: 'title',
            right: 'next'
        },

        dayCellContent: function(e) {
            e.dayNumberText = e.dayNumberText.replace('日', '');
        },

        buttonText: {
            today: '今月',
            month: '月',
            list: 'リスト'
        },

        dayMaxEvents: 3, // trueにすると月表示の際のイベントの数が曜日セルの高さに制限されイベントが多い場合は+more表記でpopoverで表示される 5未満にしたい場合は数値を指定する

        /*
        // 日付をクリック、または範囲を選択したイベント
        selectable: true,
        select: function (info) {
            // alert("selected " + info.startStr + " to " + info.endStr);

            // 入力ダイアログ
            const eventName = prompt("イベントを入力してください");

            if (eventName) {
                // イベントの追加
                calendar.addEvent({
                    title: eventName,
                    start: info.start,
                    end: info.end,
                    allDay: true,
                });
                window.open('http://127.0.0.1:8000/post_schedule/', '_blank')
            }
        },

        eventClick: function(info) {
            //クリックしたイベントのタイトルが取れるよ
            alert('Clicked on: ' + info);
        },
        */

        events: function (info, successCallback, failureCallback) {

            axios
                .post("/schedule/calendar/", {
                    start_date: info.start.valueOf(),
                    end_date: info.end.valueOf(),
                })
                .then((response) => {
                    calendar.removeAllEvents();
                    successCallback(response.data);
                })
                .catch(() => {
                    // バリデーションエラーなど
                    alert("登録に失敗しました");
                });
        },


    });

    calendar.render();
});