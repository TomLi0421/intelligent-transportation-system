import { useEffect, useState } from "react";
import "./App.css";
import DriverTable from "./components/DriverTable";
import LineChart from "./components/LineChart";
import OverspeedList from "./components/OverspeedHistory/OverspeedHistoryList";
import axios from "axios";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";

function App() {
  const [driverData, setDriverData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getDriverData();
    setInterval(() => {
      getDriverData();
    }, 30000);
  }, []);

  const getDriverData = async () => {
    const response = await axios(
      "http://comp4442-project-env.eba-kzdmamxf.us-east-1.elasticbeanstalk.com/car_speed_monitor"
    );

    setDriverData(response.data);
    setIsLoading(false);
  };

  return (
    <div className="px-10 py-12">
      <h1 className="mb-5 font-medium text-4xl">
        Intelligent Transportation System
      </h1>

      <div className="bg-white p-8 rounded-lg">
        <h2 className="font-medium text-xl mb-5">
          Real Time Driving Speed Monitoring
        </h2>
        {isLoading && driverData ? (
          <Box sx={{ display: "flex", justifyContent: "center" }}>
            <CircularProgress />
          </Box>
        ) : (
          <LineChart driverData={driverData} />
        )}
      </div>

      <div className="grid gap-x-10 mt-10 grid-cols-1 sm:grid-cols-4">
        <DriverTable />
        <div className="bg-white p-8 rounded-lg mt-10 sm:mt-0">
          <h2 className="font-medium text-xl mb-5">Overspeed History</h2>
          {isLoading && driverData ? (
            <Box sx={{ display: "flex", justifyContent: "center" }}>
              <CircularProgress />
            </Box>
          ) : (
            <OverspeedList driverData={driverData} />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
