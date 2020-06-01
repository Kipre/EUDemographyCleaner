var weights = [0.00454249931499362, 1.1196759939193726, -0.2207794487476349, 0.0996064841747284];

var weightsT = [-0.001737720682285726, 1.1234612464904785, 0.0006858287379145622, -0.08383361250162125, -0.003659510286524892, 0.0, 0.0, 0.0025732512585818768, 0.0, 0.0]

var cumulative = [0.00138954, 0.00195484, 0.00282654, 0.00383201, 0.00486769, 0.00731017, 0.00878601, 0.01079696, 0.01333005, 0.01664854, 0.02000587, 0.02538709, 0.03182556, 0.0395802, 0.04379628, 0.05377764, 0.06521758, 0.07620872, 0.09129943, 0.10679147, 0.12074293, 0.13595878, 0.15411337, 0.17707956, 0.20291112, 0.23120674, 0.25519997, 0.27586609, 0.29851725, 0.32100012, 0.34776811, 0.3732674, 0.39904718, 0.42156025, 0.43903734, 0.45652737, 0.47716327, 0.49730723, 0.51709302, 0.53782818, 0.55645314, 0.57198402, 0.5850983, 0.60165191, 0.61979355, 0.63684342, 0.65709958, 0.67475791, 0.68836414, 0.7011893, 0.71269829, 0.72903613, 0.74410957, 0.75917439, 0.7723232, 0.78205858, 0.79383512, 0.80837778, 0.81979614, 0.83283276, 0.84300399, 0.85303281, 0.86053717, 0.86956053, 0.8785623, 0.8866406, 0.89512023, 0.90331935, 0.90931334, 0.91458236, 0.91922134, 0.92545268, 0.93149846, 0.9372249, 0.9418984, 0.94535929, 0.9485699, 0.95461999, 0.958452, 0.96273281, 0.96613761, 0.96991352, 0.97282637, 0.97477258, 0.97828095, 0.98115064, 0.98392108, 0.98673468, 0.98962163, 0.99191307, 0.99320767, 0.99492086, 0.99744101, 1.];

var c = 10,
    dt = 0.005,
    yb = 1.3,
    N = 20;

function combRep(arr, l) {
    if (l === void 0)
        l = arr.length;
    // Length of the combinations
    var data = Array(l), // Used to store state
        results = [];
    // Array of results
    (function f(pos, start) {
        // Recursive function
        if (pos === l) {
            // End reached
            results.push(data.slice());
            // Add a copy of data to results
            return;
        }
        for (var i = start; i < arr.length; ++i) {
            data[pos] = arr[i];
            // Update data
            f(pos + 1, i);
            // Call f recursively
        }
    })(0, 0);
    // Start at index 0
    return results;
    // Return results
}

function augment(x, maxDegree = 3) {
    x = [1, ...x];
    return combRep(x, maxDegree).map((c) => c.reduce((a, b) => a * b));
}

function F(x, y, weights) {
    const aug = augment([y]);
    const u = weights.map((e, i) => e * aug[i]).reduce((x, y) => x + y) - y
    return [1 * 20, u * 20];
}

function fTime(t, y, weights) {
    const aug = augment([y, t]);
    const u = weights.map((e, i) => e * aug[i]).reduce((x, y) => x + y) - y
    return [1 * 20, u * 20];
}

function animation(canvasId, field, margin, xb) {
    var X0 = [],
        Y0 = [],
        X = [],
        Y = [],
        xp = d3.range(N).map((i) => xb * (i / N)),
        yp = d3.range(N).map((i) => yb * (i / N));

    // array of starting positions for each curve on a uniform grid
    for (var i = 0; i < N; i++) {
        for (var j = 0; j < N; j++) {
            X.push(xp[j]),
                Y.push(yp[i]);
            X0.push(xp[j]),
                Y0.push(yp[i]);
        }
    }

    //// frame setup
    var cvs = d3.select(canvasId).node();

  // Make it visually fill the positioned parent
  cvs.style.width ='100%';
  cvs.style.height='100%';
  // ...then set the internal size to match
  cvs.width  = cvs.offsetWidth;
  cvs.height = cvs.offsetHeight;
  
    var g = cvs.getContext("2d"), // initialize a "canvas" element
        width = cvs.width,
        height = cvs.height;
    g.clearRect(0, 0, width, height)
    g.fillStyle = "rgba(255, 255, 255, 0.05)";
    // for fading curves
    g.lineWidth = 0.7;
    g.strokeStyle = "#000000";
    // html color code
    //// mapping from vfield coords to web page coords
    var xMap = d3.scaleLinear().domain([0, xb]).range([margin.left, width - margin.right]),
        yMap = d3.scaleLinear().domain([0, yb]).range([height - margin.bottom, margin.top]);
    //// animation setup
    var animAge = 0,
        frameRate = 30, // ms per timestep (yeah I know it's not really a rate)
        M = X.length,
        MaxAge = 100, // # timesteps before restart
        age = [];
    for (var i = 0; i < M; i++) {
        age.push(randage());
    }
    var drawFlag = true;
    // setInterval(function () {if (drawFlag) {draw();}}, frameRate);
    var timer = d3.timer(function() {
        if (drawFlag) {
            draw();
        }
    }, frameRate);
    d3.select(canvasId).on("click", function() {
        drawFlag = (drawFlag) ? false : true;
    })

    function randage() {
        // to randomize starting ages for each curve
        return Math.round(Math.random() * 100);
    }
    // for info on the global canvas operations see
    // http://bucephalus.org/text/CanvasHandbook/CanvasHandbook.html#globalcompositeoperation
    g.globalCompositeOperation = "source-over";

    function draw() {
        g.fillRect(0, 0, width, height);
        // fades all existing curves by a set amount determined by fillStyle (above), which sets opacity using rgba
        for (var i = 0; i < M; i++) {
            // draw a single timestep for every curve
            var dr = field(X[i], Y[i]);
            g.beginPath();
            g.moveTo(xMap(X[i]), yMap(Y[i]));
            // the start point of the path
            g.lineTo(xMap(X[i] += dr[0] * dt), yMap(Y[i] += dr[1] * dt));
            // the end point
            g.stroke();
            // final draw command
            if (age[i]++ > MaxAge) {
                // incriment age of each curve, restart if MaxAge is reached
                age[i] = randage();
                X[i] = X0[i],
                    Y[i] = Y0[i];
            }
        }
    }
    return [width, height, timer];
}

var chart = function(svgId, data, width, height, margin, yTicks = true, title) {
    width = width - margin.left - margin.right;
    height = height - margin.top - margin.bottom;
    // append the svg object to the body of the page
    d3.select(svgId).selectAll("*").remove();
    var svg = d3.select(svgId).append("svg").attr("width", width + margin.left + margin.right).attr("height", height + margin.top + margin.bottom).append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    // Add X axis --> it is a date format
    var x = d3.scaleLinear().domain(d3.extent(data, (d) => d[0])).range([0, width]);
    var y = d3.scaleLinear().domain([0, 1.3]).range([height, 0]);
    svg.append("g").attr("transform", "translate(0," + height + ")").call(d3.axisBottom(x));
    // Add the line
    svg.append("path").datum(data).attr("fill", "none").attr("stroke", "#69b3a2").attr("stroke-width", 1.5).attr("d", d3.line().x((d) => x(d[0])).y((d) => y(d[1])))
    // Add the points
    svg.append("g").selectAll("dot").data(data).enter().append("circle").attr("cx", (d) => x(d[0])).attr("cy", (d) => y(d[1])).attr("r", 2).attr("fill", "#69b3a2")

    // Add Title
    svg.append("text").attr("text-anchor", "middle").attr("x", (width) / 2).attr("y", height + margin.top + 35).text(title).style("font-size", "18px");

    if (yTicks) {
        // Y axis label:
        svg.append("text").attr("text-anchor", "end").attr("transform", "rotate(-90)").attr("y", -margin.left + 20).attr("x", -margin.top).text("Cumulative cases")
        // Add Y axis
        svg.append("g").call(d3.axisLeft(y));
    } else {
        // Add X axis label:
        svg.append("text").attr("text-anchor", "end").attr("x", width).attr("y", height + margin.top + 20).text("Days");
        // Add legend
        const legendPosition = {
            x: 90,
            y: 15
        }

        var rect = {
            width: 95,
            height: 30
        }

        svg.append('rect').attr('x', width + margin.left - legendPosition.x - 10).attr('y', margin.top + legendPosition.y - rect.height / 2).attr('width', rect.width).attr('height', rect.height).attr('rx', 5).attr('ry', 5).style('fill', 'white').style('stroke', 'black').style('opacity', 0.5)
        svg.append("circle").attr("cx", width + margin.left - legendPosition.x).attr("cy", margin.top + legendPosition.y).attr("r", 4).style("fill", "#69b3a2")

        svg.append("text").attr("x", width + margin.left - legendPosition.x + 20).attr("y", margin.top + legendPosition.y).text("real data").attr("alignment-baseline", "middle")

    }
}

var marginLeft = {
    top: 10,
    right: 3,
    bottom: 50,
    left: 50
};
var marginRight = {
    top: 10,
    right: 50,
    bottom: 50,
    left: 3
};

var countrySelector = document.querySelector('.countrydata');

function assignOptions(textArray, selector) {
    for (var i = 0; i < textArray.length; i++) {
        var currentOption = document.createElement('option');
        currentOption.text = textArray[i];
        selector.appendChild(currentOption);
    }
}

var allData;

var width, height, timer1 = null, timer2 = null;

d3.json("https://raw.githubusercontent.com/Kipre/files/master/internship/data/time-dependent.json").then((data) => {
    listofCountries = Object.keys(data);
    
    assignOptions(listofCountries, countrySelector);

    allData = data;
    updateCountry = () => {
        if (timer1 != null) {
            timer1.stop();
            delete timer1;
            timer2.stop();
            delete timer2;
        }
        var country = countrySelector.value;
        [width, height, timer1] = animation('#independent', (x, y) => F(x, y, allData[country]['independent']), marginLeft, allData[country]['data'].length);
        [_, _, timer2] = animation('#dependent', (x, y) => fTime(x, y, allData[country]['dependent']), marginRight, allData[country]['data'].length);

        chart("#svg-independent", allData[country]['data'].map((e, i) => [i, e]), width, height, marginLeft, yTicks = true, 'Time-invariant')
        chart("#svg-dependent", allData[country]['data'].map((e, i) => [i, e]), width, height, marginRight, yTicks = false, 'Time-dependent')

    }

    countrySelector.addEventListener('change', updateCountry, false);
    window.onresize = updateCountry;
    updateCountry();

});