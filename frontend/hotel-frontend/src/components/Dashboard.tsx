import { Card, Grid, Box, Typography, CircularProgress } from "@mui/material";
import { useSelector, useDispatch } from "react-redux";
import { useEffect } from "react";
import { fetchStats, fetchRecentBookings } from "../api";

interface DashboardStats {
  total_rooms: number;
  available_rooms: number;
  occupied_rooms: number;
  reserved_rooms: number;
  total_customers: number;
  active_bookings: number;
  today_checkins: number;
  today_checkouts: number;
  total_payments: number;
  revenue: number;
}

export default function Dashboard() {
  const dispatch = useDispatch();
  const stats = useSelector((state: any) => state.dashboard.stats);
  const loading = useSelector((state: any) => state.dashboard.loading);
  const error = useSelector((state: any) => state.dashboard.error);
  const recentBookings = useSelector((state: any) => state.dashboard.recentBookings);

  useEffect(() => {
    dispatch(fetchStats());
    fetchRecentBookings();
  }, [dispatch]);

  if (loading) {
    return (
    );
  }
  }
  return (
    <div className="p-4">
      <h2 className="mb-4 text-xl font-bold">Dashboard</h2>
      
      {loading && (
        <div className="flex justify-center py-8">
          <CircularProgress />
        </div>
      )}

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-800 rounded">
          {error}
        </div>
      )}

      <Grid className="grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
        {Object.entries(stats).map(([key, value]) => (
          <Card key={key} className="p-4">
            <Typography variant="subtitle1" className="text-muted-text">
              {key.replace(/_/g, " ")}
            </Typography>
            <Typography variant="h4" className="mt-2">
              {value}
            </Typography>
          </Card>
        ))}
      </Grid>

      <Grid className="grid-cols-1 md:grid-cols-2 gap-4 mt-6">
        <Card className="p-4">
          <Typography variant="h6">Recent Bookings</Typography>
          {recentBookings.map((booking: any) => (
            <div key={booking.id} className="p-3 border rounded mb-2">
              <strong>#{booking.booking_reference}</strong> - {booking.customer_name} - {booking.room_number}
            </div>
          ))}
        </Card>
      </Grid>
    </div>
  );
}