from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


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
    <h1>Data Visualization</h1>
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
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        var cal = new CalHeatMap();
        cal.init({
            itemSelector: "#heatmapContainer",
            domain: "day",
            domainGutter: 2,
            data: 'http://localhost:8000/api/records/heatmap/',
            dataType: "json",
            start: new Date(new Date().setDate(new Date().getDate() - 5)),
            cellSize: 20,
            range: 12,
            legend: [2, 4, 6, 8]
        });

        var ws = new WebSocket('ws://localhost:8000/ws');
        ws.onmessage = function(event) {
            var data = JSON.parse(event.data);
            // Update your charts with the new data
        };

        fetch('/api/records')
            .then(response => response.json())
            .then(data => {
                // Assuming data is an array of records
                var labels = data.map(record => record.created_at); // Adjust according to your data structure
                var chartData = data.map(record => record.seen ? 1 : 0); // Adjust according to your data structure

                lineChart.data.labels = labels;
                lineChart.data.datasets[0].data = chartData;
                lineChart.update();
            })
            .catch(error => console.error('Error fetching records:', error));

    </script>
</body>
</html>
"""

@view_router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return HTMLResponse(content=LOGIN_HTML)

@view_router.get("/data", response_class=HTMLResponse)
async def data_page(request: Request):
    return HTMLResponse(content=DATA_HTML)