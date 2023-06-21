html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Orders</title>
        <style>
            table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            
            }

            td, th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
            }

            tr:nth-child(even) {
            background-color: #dddddd;
            }
        </style>
    </head>
    <body>
        <h1>WebSocket Orders</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label for="stoks">Stoks:</label><br>
            <input type="text" id="stoks" value="EURUSD" autocomplete="off"/><br>
            <label for="quantity">Quantity:</label><br>
            <input type="text" id="quantity" value="100" autocomplete="off"/>
            <button>Place order</button>
        </form>
        <br>
        <table id="orders">
            <tr>
                <th>id</th>
                <th>Stoks</th>
                <th>Quantity</th>
                <th>Status</th>
            </tr>
        </table>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var orders = document.getElementById('orders');
                var newRow = document.createElement("tr");
                var id = document.createElement("td");
                var stoks = document.createElement("td");
                var quantity = document.createElement("td");
                var status = document.createElement("td");
                var data = JSON.parse(event.data);
                id.textContent = data["id"];
                stoks.textContent = data["stoks"];
                quantity.textContent = data["quantity"];
                status.textContent = data["status"];

                newRow.appendChild(id);
                newRow.appendChild(stoks);
                newRow.appendChild(quantity);
                newRow.appendChild(status);
                orders.appendChild(newRow);
                var newRow = document.createElement("tr");
            };
            function sendMessage(event) {
                var stoks = document.getElementById("stoks")
                var quantity = document.getElementById("quantity")
                var response = {"stoks": stoks.value, "quantity": quantity.value};
                ws.send(JSON.stringify(response));
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

html_orders = """
<!DOCTYPE html>
<html>
    <head>
        <title>Orders</title>
    </head>
    <body>
        <div id="executed">
            EXECUTED ORDERS (STATUS CHANGED TO EXECUTED)<br><br>
        </div>
        <form action="" onsubmit="executeOrder(event)">
            <button>Execute random orders</button>
        </form>
        <div id="orders">
        </div>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/orders/execute");
            ws.onmessage = function(event) {
                var executed = document.getElementById("executed");
                var data = JSON.parse(event.data);
                var content = ""
                for (var key in data) {
                    content += key + " - " + data[key] + "<br>";
                }
                executed.innerHTML += content
            };
            function executeOrder(event) {
                ws.send("trigger execution");
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""