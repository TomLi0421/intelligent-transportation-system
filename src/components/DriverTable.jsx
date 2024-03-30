import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";

export default function BasicTable({ summaryData }) {
  return (
    <TableContainer className="rounded-lg">
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
            <TableCell>Cumulative number of overspeed</TableCell>
            <TableCell>Fatigue driving</TableCell>
            <TableCell>Total time of overspeed(s)</TableCell>
            <TableCell>Netural slide(mins)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {summaryData.map((driver, index) => (
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
              <TableCell>{driver.overspeed.cumulativeTimes}</TableCell>
              <TableCell>{driver.fatigueDriving.cumulativeTimes}</TableCell>
              <TableCell>{driver.overspeed.totalTime}</TableCell>
              <TableCell>{driver.neutralSlide.totalTime}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
