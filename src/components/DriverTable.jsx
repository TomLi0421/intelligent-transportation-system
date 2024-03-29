import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

function createData(name, calories, fat, carbs, protein) {
  return { name, calories, fat, carbs, protein };
}

const rows = [
  createData("Frozen yoghurt", 159, 6.0, 24, 4.0),
  createData("Ice cream sandwich", 237, 9.0, 37, 4.3),
  createData("Eclair", 262, 16.0, 24, 6.0),
  createData("Cupcake", 305, 3.7, 67, 4.3),
  createData("Gingerbread", 356, 16.0, 49, 3.9),
];

export default function BasicTable() {
  return (
    <TableContainer component={Paper}>
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
            "& .MuiTableSortLabel-root.Mui-active, .MuiTableSortLabel-root.Mui-active .MuiTableSortLabel-icon":
              {
                color: "red",
              },
          }}
        >
          <TableRow>
            <TableCell>#</TableCell>
            <TableCell>Driver id</TableCell>
            <TableCell>Car plate number</TableCell>
            <TableCell>Cumulative number of overspeed</TableCell>
            <TableCell>Fatigue driving</TableCell>
            <TableCell>Total time of overspeed and netural slide(s)</TableCell>
            <TableCell align="right">Netural slide(s)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row, index) => (
            <TableRow
              key={row.name}
              sx={{
                "&:last-child td, &:last-child th": { border: 0 },
                "&:nth-child(2n) th, &:nth-child(2n) td": {
                  backgroundColor: "#F4F7FC",
                },
                "&:nth-child(1n) th, &:nth-child(1n) td": {
                  backgroundColor: "white",
                },
                "&:nth-child(n) th, &:nth-child(n) td": {
                  fontSize: 14,
                  color: "#464F60",
                  fontWeight: 400,
                },
              }}
            >
              <TableCell component="th" scope="row">
                {index + 1}
              </TableCell>
              <TableCell>{row.calories}</TableCell>
              <TableCell>{row.calories}</TableCell>
              <TableCell>{row.fat}</TableCell>
              <TableCell>{row.carbs}</TableCell>
              <TableCell>{row.protein}</TableCell>
              <TableCell>{row.protein}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
