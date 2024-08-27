import { useEffect, useState } from "react"
import { TrendingUp } from "lucide-react"
import { CartesianGrid, Line, LineChart, XAxis, YAxis, Tooltip, Legend } from "recharts"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./components/ui/card"

interface SimulationResult {
  timestamp: string
  win_probabilities: {
    "Donald Trump": number
    "Kamala Harris": number
  }
}

function App() {
  const [chartData, setChartData] = useState<SimulationResult[]>([])

  useEffect(() => {
    fetch('/simulation_results.json')
      .then(response => response.json())
      .then(data => setChartData(data))
      .catch(error => console.error('Error fetching data:', error))
  }, [])

  const formattedData = chartData.map(result => ({
    timestamp: new Date(result.timestamp).toLocaleDateString(),
    "Donald Trump": result.win_probabilities["Donald Trump"] * 100,
    "Kamala Harris": result.win_probabilities["Kamala Harris"] * 100,
  }))

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>2024 Election Win Probability</CardTitle>
          <CardDescription>August 23 - August 27, 2024</CardDescription>
        </CardHeader>
        <CardContent>
          <LineChart
            width={600}
            height={300}
            data={formattedData}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="timestamp" />
            <YAxis domain={[40, 60]} tickFormatter={(value) => `${value}%`} />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="Donald Trump"
              stroke="#FF0000"
              strokeWidth={2}
              dot={false}
            />
            <Line
              type="monotone"
              dataKey="Kamala Harris"
              stroke="#0000FF"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </CardContent>
        <CardFooter>
          <div className="flex w-full items-start gap-2 text-sm">
            <div className="grid gap-2">
              <div className="flex items-center gap-2 font-medium leading-none">
                Win probabilities fluctuating <TrendingUp className="h-4 w-4" />
              </div>
              <div className="flex items-center gap-2 leading-none text-muted-foreground">
                Showing win probabilities based on simulation results
              </div>
            </div>
          </div>
        </CardFooter>
      </Card>
    </div>
  )
}

export default App