$(document).ready(function() {
	$(chart_id).highcharts({
		chart: chart,
		title: title,
		xAxis: xAxis,
		yAxis: yAxis,
        series: series,
        credits: credits,
        legend: legend,
        backgroundColor: backgroundColor
	});
});