import { useEffect, useState } from 'react'
import './App.css'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card'
import { ChartContainer, ChartConfig, ChartTooltip, ChartTooltipContent } from './components/ui/chart'
import { LineChart, Line, XAxis, CartesianGrid, YAxis, ResponsiveContainer, Tooltip, Legend } from 'recharts'

interface SimulationResult {
  timestamp: string;
  win_probabilities: {
    'Donald Trump': number;
    'Kamala Harris': number;
  };
}

const chartConfig = {
  'Donald Trump': {
    label: "Donald Trump",
    color: "hsl(var(--chart-1))",
  },
  'Kamala Harris': {
    label: "Kamala Harris",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig

function App() {
  const [simulationData, setSimulationData] = useState<SimulationResult[]>([])

  useEffect(() => {
    fetch('/simulation_results.json')
      .then(response => response.json())
      .then(data => {
        console.log('Raw data:', data); // Log raw data
        const formattedData = data.map((item: SimulationResult) => ({
          timestamp: new Date(item.timestamp).toLocaleDateString(),
          'Donald Trump': item.win_probabilities['Donald Trump'] * 100,
          'Kamala Harris': item.win_probabilities['Kamala Harris'] * 100,
        }))
        console.log('Formatted data:', formattedData); // Log formatted data
        setSimulationData(formattedData)
      })
      .catch(error => console.error('Error loading simulation data:', error))
  }, [])

  console.log('Render data:', simulationData); // Log data on each render

  return (
    <div className="container mx-auto p-4">
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Election Simulation Results</CardTitle>
          <CardDescription>Percentage chance of winning over time</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <ChartContainer config={chartConfig}>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={simulationData}>
                <CartesianGrid vertical={false} stroke="hsl(var(--primary-foreground) / 0.1)" />
                <XAxis
                  dataKey="timestamp"
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  tickFormatter={(value) => value.slice(0, 3)}
                  stroke="hsl(var(--primary-foreground))"
                />
                <YAxis
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  tickFormatter={(value) => `${value}%`}
                  stroke="hsl(var(--primary-foreground))"
                />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="Donald Trump"
                  stroke="var(--color-Donald Trump)"
                  strokeWidth={2}
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="Kamala Harris"
                  stroke="var(--color-Kamala Harris)"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </ChartContainer>
        </CardContent>
      </Card>
    </div>
  )
}

export default App