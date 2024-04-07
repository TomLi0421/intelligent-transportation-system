import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import axios from "axios";
import { useEffect, useState } from "react";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";

export default function BasicTable() {
  const [driverData, setDriverData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getDriverData();
  }, []);

  const getDriverData = async () => {
    const response = await axios.get(
      "http://comp4442-project-env.eba-kzdmamxf.us-east-1.elasticbeanstalk.com/summary"
    );

    setDriverData(response.data);
    setIsLoading(false);
  };

  return (
    <div className="bg-white p-8 rounded-lg xl:col-span-3">
      <h2 className="font-medium text-xl mb-5">Driver Behaviour Summary</h2>
      {isLoading ? (
        <Box sx={{ display: "flex", justifyContent: "center" }}>
          <CircularProgress />
        </Box>
      ) : (
        <TableContainer>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead
              sx={{
                "& th": {
                  color: "#464F60",
                  backgroundColor: "#F4F7FC",
                  textTransform: "uppercase",
                  fontSize: 11,
                  fontWeight: 600,
                },
              }}
            >
              <TableRow>
                <TableCell>#</TableCell>
                <TableCell>Driver id</TableCell>
                <TableCell>Car plate number</TableCell>
                <TableCell>Average speed (km/h)</TableCell>
                <TableCell>Cumulative number of overspeed</TableCell>
                <TableCell>Cumulative total time of overspeed (mins)</TableCell>
                <TableCell>Fatigue driving count</TableCell>
                <TableCell>Throttle stop count</TableCell>
                <TableCell>Oil leak count</TableCell>
                <TableCell>Netural slide (mins)</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {driverData.map((driver, index) => (
                <TableRow
                  key={driver.driverId}
                  sx={{
                    "&:last-child td, &:last-child th": { border: 0 },
                    "&:nth-of-type(1n) td, &:nth-of-type(1n) th": {
                      color: "#171C26",
                      fontSize: 14,
                      fontWeight: 400,
                    },
                    "&:nth-of-type(even) td, &:nth-of-type(even) th": {
                      backgroundColor: "#F9FAFC",
                    },
                    "&:nth-of-type(odd) td, &:nth-of-type(odd) th": {
                      backgroundColor: "white",
                    },
                  }}
                >
                  <TableCell component="th" scope="row">
                    {index + 1}
                  </TableCell>
                  <TableCell>{driver.driverId}</TableCell>
                  <TableCell>{driver.carPlateNumber}</TableCell>
                  <TableCell>{driver.avgSpeed}</TableCell>
                  <TableCell>{driver.overspeedCount}</TableCell>
                  <TableCell>
                    {(driver.overspeedTotalTime / 60).toFixed(2)}
                  </TableCell>
                  <TableCell>{driver.fatigueDrivingCount}</TableCell>
                  <TableCell>{driver.hthrottleStopCount}</TableCell>
                  <TableCell>{driver.oilLeakDrivingCount}</TableCell>
                  <TableCell>
                    {(driver.neutralSlide_totalTime / 60).toFixed(2)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </div>
  );
}
