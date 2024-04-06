import React, { useState, useEffect } from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";

function LineChart() {
  const options = {
    title: null,
    series: [
      {
        data: [1, 2, 3],
      },
      {
        data: [5, 4, 6],
      },
    ],
  };
  return (
    <div className="bg-white p-8 rounded-lg col-span-2">
      <h2 className="font-medium text-xl mb-5">
        Real Time Driving Speed Monitoring
      </h2>
      <HighchartsReact highcharts={Highcharts} options={options} />
    </div>
  );
}

export default LineChart;
