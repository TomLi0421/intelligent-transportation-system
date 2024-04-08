import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";

function LineChart({ driverData }) {
  let seriesData = [];
  let driverSet = new Set();

  for (let i = 0; i < driverData.length; i++) {
    if (!driverSet.has(driverData[i].DriverID)) {
      driverSet.add(driverData[i].DriverID);

      const driverSpeedData = driverData
        .filter((driver) => driver.DriverID === driverData[i].DriverID)
        .map((driver) => [
          new Date(driver.CurrentTime).getTime(),
          driver.Speed,
        ]);
      const driverID = driverData[i].DriverID;
      seriesData.push({
        type: "spline",
        name: driverID,
        data: driverSpeedData,
      });
    }
  }

  console.log(seriesData);

  const minAndMaxTime = driverData
    .filter((driver) => driver.DriverID === driverData[0].DriverID)
    .map((driver) => new Date(driver.CurrentTime).getTime());

  const minTime = Math.min(...minAndMaxTime.map((data) => data));
  const maxTime = Math.max(...minAndMaxTime.map((data) => data));

  let options = {
    title: null,
    xAxis: {
      type: "datetime",
      min: minTime,
      max: maxTime,
      title: {
        text: "Time",
      },
    },
    yAxis: {
      title: {
        text: "Driving Speed (km/h)",
      },
    },
    series: [...seriesData],
  };

  return <HighchartsReact highcharts={Highcharts} options={options} />;
}

export default LineChart;
