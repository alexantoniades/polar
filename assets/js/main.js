var data;
const submitEvent = () => {
    const command = document.querySelector('#command').value;
    axios.get('/api', {
        params: {
            command: command,
            user: 71
        }    
    })
    .then(function (response) {
    data = response.data;
    // Bar Chart
    var chart_bar = new Chart(document.getElementById('chart-bar').getContext('2d'), {
        type: 'bar',
        data: {
            labels: ['Neutral', 'Suspicious'],
            datasets: [{
                label: 'Propability of being neutral or suspicious',
                data: [data.neutral, data.suspicious],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    // Doughnut Chart
    var topRightChart = new Chart(document.getElementById('chart-doughnut').getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Total commands', ...data.command.split(' ')],
            datasets: [{
                label: 'Propability of being neutral or suspicious',
                data: [data.totalCommands, ...data.occurrencesInteger],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(127, 165, 64, 0.2)',
                    'rgba(255, 123,  64, 0.2)',
                    'rgba(34, 117, 200, 0.2)',
                    'rgba(200, 34, 200, 0.2)',
                    'rgba(113, 19, 113, 0.2)',
                    'rgba(73, 59, 73, 0.2)',
                    'rgba(61, 61, 167, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(127, 165, 64, 0.2)',
                    'rgba(255, 123,  64, 0.2)',
                    'rgba(34, 117, 200, 0.2)',
                    'rgba(200, 34, 200, 0.2)',
                    'rgba(113, 19, 113, 0.2)',
                    'rgba(73, 59, 73, 0.2)',
                    'rgba(61, 61, 167, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(127, 165, 64, 1)',
                    'rgba(255, 123,  64, 1)',
                    'rgba(34, 117, 200, 1)',
                    'rgba(200, 34, 200, 1)',
                    'rgba(113, 19, 113, 1)',
                    'rgba(73, 59, 73, 1)',
                    'rgba(61, 61, 167, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(127, 165, 64, 1)',
                    'rgba(255, 123,  64, 1)',
                    'rgba(34, 117, 200, 1)',
                    'rgba(200, 34, 200, 1)',
                    'rgba(113, 19, 113, 1)',
                    'rgba(73, 59, 73, 1)',
                    'rgba(61, 61, 167, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    Sticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    // Pie Chart
    var bottomLeftChart = new Chart(document.getElementById('chart-pie').getContext('2d'), {
        type: 'pie',
        data: {
            labels: ['Average occurence', ...data.command.split(' ')],
            datasets: [{
                label: 'Comparison of the average joined occurence vs individual occurence',
                data: [data.occurrencesAverage, ...data.occurrencesFloat],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(127, 165, 64, 0.2)',
                    'rgba(255, 123,  64, 0.2)',
                    'rgba(34, 117, 200, 0.2)',
                    'rgba(200, 34, 200, 0.2)',
                    'rgba(113, 19, 113, 0.2)',
                    'rgba(73, 59, 73, 0.2)',
                    'rgba(61, 61, 167, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(127, 165, 64, 0.2)',
                    'rgba(255, 123,  64, 0.2)',
                    'rgba(34, 117, 200, 0.2)',
                    'rgba(200, 34, 200, 0.2)',
                    'rgba(113, 19, 113, 0.2)',
                    'rgba(73, 59, 73, 0.2)',
                    'rgba(61, 61, 167, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(127, 165, 64, 1)',
                    'rgba(255, 123,  64, 1)',
                    'rgba(34, 117, 200, 1)',
                    'rgba(200, 34, 200, 1)',
                    'rgba(113, 19, 113, 1)',
                    'rgba(73, 59, 73, 1)',
                    'rgba(61, 61, 167, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(127, 165, 64, 1)',
                    'rgba(255, 123,  64, 1)',
                    'rgba(34, 117, 200, 1)',
                    'rgba(200, 34, 200, 1)',
                    'rgba(113, 19, 113, 1)',
                    'rgba(73, 59, 73, 1)',
                    'rgba(61, 61, 167, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    Sticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    })
    .catch(function (error) {
    console.log(error);
    });
};

document.querySelector('#command').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      submitEvent();
    }
});
document.querySelector('#submit-btn').addEventListener('click', submitEvent)
