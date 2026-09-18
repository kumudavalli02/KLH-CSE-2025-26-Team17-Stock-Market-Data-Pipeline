let stockChart = null;


async function runPipeline() {

    const symbol =
        document.getElementById("symbol").value;

    const period =
        document.getElementById("period").value;


    try {

        const response =
            await fetch(
                `/api/stock?symbol=${symbol}&period=${period}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            alert(data.error);

            return;
        }


        document.getElementById(
            "stockName"
        ).textContent = data.symbol;


        document.getElementById(
            "latestPrice"
        ).textContent =
            "₹" +
            data.latest.close.toFixed(2);


        document.getElementById(
            "change"
        ).textContent =
            data.latest.change.toFixed(2)
            +
            " ("
            +
            data.latest.change_pct.toFixed(2)
            +
            "%)";


        document.getElementById(
            "records"
        ).textContent =
            data.records;


        document.getElementById(
            "missing"
        ).textContent =
            data.pipeline.missing_values;


        document.getElementById(
            "duplicates"
        ).textContent =
            data.pipeline.duplicate_rows;


        document.getElementById(
            "latestData"
        ).innerHTML = `

            <strong>Date:</strong>
            ${data.latest.date}
            <br>

            <strong>Open:</strong>
            ₹${data.latest.open.toFixed(2)}
            <br>

            <strong>High:</strong>
            ₹${data.latest.high.toFixed(2)}
            <br>

            <strong>Low:</strong>
            ₹${data.latest.low.toFixed(2)}
            <br>

            <strong>Close:</strong>
            ₹${data.latest.close.toFixed(2)}
            <br>

            <strong>Volume:</strong>
            ${data.latest.volume.toLocaleString()}
            <br>

            <strong>MA20:</strong>
            ${
                data.latest.ma20
                ?
                "₹" +
                data.latest.ma20.toFixed(2)
                :
                "N/A"
            }
            <br>

            <strong>MA50:</strong>
            ${
                data.latest.ma50
                ?
                "₹" +
                data.latest.ma50.toFixed(2)
                :
                "N/A"
            }

        `;


        createChart(data);


    } catch (error) {

        console.error(error);

        alert(
            "Unable to fetch stock data."
        );
    }
}


function createChart(data) {

    const ctx =
        document
            .getElementById("stockChart")
            .getContext("2d");


    if (stockChart) {

        stockChart.destroy();
    }


    stockChart = new Chart(
        ctx,
        {

            type: "line",

            data: {

                labels:
                    data.chart.dates,

                datasets: [

                    {
                        label: "Closing Price",

                        data:
                            data.chart.close,

                        tension: 0.3
                    },

                    {
                        label: "MA20",

                        data:
                            data.chart.ma20,

                        tension: 0.3
                    },

                    {
                        label: "MA50",

                        data:
                            data.chart.ma50,

                        tension: 0.3
                    }

                ]
            },

            options: {

                responsive: true,

                interaction: {
                    mode: "index",
                    intersect: false
                },

                scales: {

                    x: {
                        ticks: {
                            maxTicksLimit: 10
                        }
                    }

                }

            }

        }
    );
}


runPipeline();