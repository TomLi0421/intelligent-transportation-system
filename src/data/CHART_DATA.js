export function generateDummyData(driverCount, dataPoints) {
  const dummyData = [];

  for (let i = 1; i <= driverCount; i++) {
    const driverData = {
      ID: i,
      DriverID: `driver${i}`,
      SpeedData: [],
    };

    let currentTime = new Date("2017-01-01T08:00:05Z");

    for (let j = 0; j < dataPoints; j++) {
      driverData.SpeedData.push({
        currentTime: currentTime.toISOString(),
        speed: Math.floor(Math.random() * 100) + 50, // random speed between 50 and 150
        isOverspeed: Math.random() > 0.5, // random boolean
      });

      currentTime.setSeconds(currentTime.getSeconds() + 30);
    }

    dummyData.push(driverData);
  }

  return dummyData;
}

const dummy_chartData = generateDummyData(5, 10);
export default dummy_chartData;
