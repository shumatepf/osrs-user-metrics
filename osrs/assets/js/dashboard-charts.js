


skill_colors = {
    "attack": ["rgba(123, 36, 29)", "rgba(217, 190, 26)"],
    "strength": ["rgba(13, 117, 77)", "rgba(139, 29, 17)"],
    "defense": ["rgba(110, 129, 193)", "rgba(203, 203, 175)"],
    "ranged": ["rgba(101, 125, 45)", "rgba(128, 67, 13)"],
    "prayer": ["rgba(236, 234, 234)", "rgba(251, 220, 37)"],
    "magic": ["rgba(52, 54, 142)", "rgba(160, 149, 128)"],
    "runecrafting": ["rgba(175, 177, 166)", "rgba(183, 125, 21)"],
    "hitpoints": ["rgba(156, 32, 17)", "rgba(255, 202, 195)"],
    "crafting": ["rgba(130, 100, 73)", "rgba(203, 178, 24)"],
    "mining": ["rgba(90, 88, 70)", "rgba(112, 172, 197)"],
    "smithing": ["rgba(90, 88, 70)", "rgba(206, 180, 22)"],
    "fishing": ["rgba(121, 152, 181)", "rgba(213, 187, 27)"],
    "cooking": ["rgba(92, 38, 107)", "rgba(137, 27, 15)"],
    "firemaking": ["rgba(205, 107, 26)", "rgba(209, 183, 24)"],
    "woodcutting": ["rgba(148, 121, 67)", "rgba(46, 102, 60)"],
    "agility": ["rgba(44, 46, 119)", "rgba(133, 40, 34)"],
    "herblore": ["rgba(13, 109, 13)", "rgba(219, 192, 26)"],
    "thieving": ["rgba(101, 57, 85)", "rgba(21, 17, 17)"],
    "fletching": ["rgba(9, 69, 72)", "rgba(203, 178, 24)"],
    "slayer": ["rgba(40, 38, 38)", "rgba(112, 24, 13)"],
    "farming": ["rgba(44, 96, 44)", "rgba(160, 186, 106)"],
    "construction": ["rgba(162, 150, 129)", "rgba(189, 134, 46)"],
    "hunter": ["rgba(110, 102, 74)", "rgba(29, 21, 0)"]
}

const myChart = new Chart("chartPreferences", {
    type: "pie",
    data: {},
    options: {
        legend: {
            display: false
        },
    }
});

function updatePIChart() {
    
    var name = $('#userName').val();
    var from = $('#fromDate').val();
    var to = $('#toDate').val();

    var d1 = new Date()
    var d2 = new Date(from)
    var d3 = new Date(to)

    var diffFrom = Math.floor(Math.abs(d1-d2)/86400000) + 1;
    var diffTo = Math.floor(Math.abs(d1-d3)/86400000) + 1;


    console.log("diffFrom = " + diffFrom)
    console.log("diffTo = " + diffTo)

    var diff = diffFrom - diffTo



    $("#numDays").text(diff)
    $("#userNameTitle").text(name)

    var getData = $.get(`search/${name}/diff?from=${diffFrom}&to=${diffTo}`)
    getData.done(function (results) {
        resultsJSON = JSON.parse(results)

        values = Object.values(resultsJSON)
        numSkills = 0

        values.forEach(element => {
            if (element > 0) {
                numSkills++
            }
        });

        $("#numSkillsIncreased").text(numSkills)

        const data = {
            labels: Object.keys(resultsJSON),
            datasets: [{
                label: 'My First Dataset',
                data: values,
                hoverOffset: 4,
                borderWidth: 1,
                backgroundColor: [],
                borderColor: []
            }]
        };
        var dataset = data.datasets[0];
        for (var i = 0; i < dataset.data.length; i++) {
            dataset.backgroundColor.push(skill_colors[data.labels[i]][0])
            //dataset.borderColor.push(skill_colors[data.labels[i]][1])
        }

        myChart.data = data
        myChart.update()
    })
}
