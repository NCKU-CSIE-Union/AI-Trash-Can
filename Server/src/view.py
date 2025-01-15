from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from src.security import is_valid_token

view_router = APIRouter()

templates = Jinja2Templates(directory="templates")

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
</head>
<body>
    <h1>Login</h1>
    <form action="/api/login" method="post">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username"><br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
"""

DATA_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Data Visualization</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script type="text/javascript" src="//d3js.org/d3.v3.min.js"></script>
    <script type="text/javascript" src="//cdn.jsdelivr.net/cal-heatmap/3.3.10/cal-heatmap.min.js"></script>
    <link rel="stylesheet" href="//cdn.jsdelivr.net/cal-heatmap/3.3.10/cal-heatmap.css" />
</head>
<body>
    <div style="margin-bottom: 20px;">
        <label for="aggregate_by">Aggregate By:</label>
        <select id="aggregate_by" name="aggregate_by" style="padding: 5px; border-radius: 5px; border: 1px solid #ccc;">
            <option value="minute" selected>Minute</option>
            <option value="hour">Hour</option>
            <option value="day">Day</option>
            <option value="month">Month</option>
        </select>
    </div>
    <div style="width: 800px; height: 400px;">
        <canvas id="lineChart"></canvas>
    </div>
    <div id="heatmapContainer" style="width: 600px; height: 200px;"></div>
    <script>
        var ctx = document.getElementById('lineChart').getContext('2d');
        var lineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [], // Add your labels here
                datasets: [{
                    label: 'Trash Count',
                    data: [], // Add your data here
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Trash Count'
                    }
                }
            }
        });
        //9467050352000
        //173693445
        var cal = new CalHeatMap();
        cal.init({
            itemSelector: "#heatmapContainer",
            domain: "day",
            subDomain: "hour",
            domainGutter: 2,
            data: 'http://localhost:8000/api/records/heatmap/',
            dataType: "json",
            start: new Date(new Date().setDate(new Date().getDate() - 5)),
            previousSelector: '#cal-HeatMap-PreviousDomain-selector',
            nextSelector: '#cal-HeatMap-NextDomain-selector',
            cellSize: 20,
            range: 12,
            legend: [1, 2, 3, 4]
        });

        var ws = new WebSocket("ws://localhost:8000/ws");
        var alertContainer = document.createElement('div');
        alertContainer.style.position = 'fixed';
        alertContainer.style.top = '10px';
        alertContainer.style.right = '10px';
        alertContainer.style.zIndex = '1000';
        document.body.appendChild(alertContainer);

        function showAlert(message) {
            var alert = document.createElement('div');
            alert.style.backgroundColor = 'rgba(0, 128, 0, 0.5)';
            alert.style.color = 'white';
            alert.style.padding = '3px';
            alert.style.paddingLeft = '10px';
            alert.style.paddingRight = '10px';
            alert.style.marginBottom = '5px';
            alert.style.borderRadius = '5px';
            alert.innerText = message;
            alertContainer.appendChild(alert);

            setTimeout(function() {
                alertContainer.removeChild(alert);
            }, 5000);
        }

        function showNewRecordAlert(data) {
            var alert = document.createElement('div');
            alert.style.backgroundColor = 'rgba(0, 128, 0, 0.5)';
            alert.style.color = 'white';
            alert.style.padding = '3px';
            alert.style.paddingLeft = '10px';
            alert.style.paddingRight = '10px';
            alert.style.marginBottom = '5px';
            alert.style.borderRadius = '5px';
            alert.innerHTML = `<h5>New Record</h5><ul><li>id: ${data.id}</li><li>created_at: ${data.created_at}</li></ul>`;
            alertContainer.appendChild(alert);

            setTimeout(function() {
                alertContainer.removeChild(alert);
            }, 3000);
        }

        function updateLineChart(aggregateBy) {
                fetch(`/api/records/line/?aggregate_by=${aggregateBy}`)
                    .then(response => {
                        console.log(response);
                        if (response.status === 401) {
                            window.location.href = "/";
                        }                        
                        return response.json();
                    })
                    .then(data => {
                        var labels = [];
                        var values = [];
                        data.forEach(function(item) {
                            labels.push(item.date);
                            values.push(item.count);
                        });
                        // reverse the order of the data
                        labels.reverse();
                        values.reverse();
                        lineChart.data.labels = labels;
                        lineChart.data.datasets[0].data = values;
                        lineChart.update();
                    })
                    .catch(error => console.error('Error fetching records:', error));
            }

        ws.onmessage = function(event) {
            var data = JSON.parse(event.data);
            if (data.event_type === "system") {
                showAlert(data.message);
            } else if (data.event_type === "new_record") {
                showNewRecordAlert(data);
                console.log(data);
                updateLineChart(document.getElementById('aggregate_by').value);
            }
        };

        document.getElementById('aggregate_by').addEventListener('change', function() {
            var aggregateBy = this.value;
            console.log(aggregateBy);
            updateLineChart(aggregateBy);
        });

        updateLineChart(document.getElementById('aggregate_by').value);

    </script>
</body>
</html>
"""


@view_router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    token = request.cookies.get("auth")
    if not token or not is_valid_token(token):
        return HTMLResponse(content=LOGIN_HTML)
    return RedirectResponse(url="/data", status_code=status.HTTP_303_SEE_OTHER)


@view_router.get("/data", response_class=HTMLResponse)
async def data_page(request: Request):
    return HTMLResponse(content=DATA_HTML)
