import { useEffect, useState, useMemo } from "react"
import {
  Bar,
  BarChart,
  CartesianGrid,
  Label,
  Line,
  LineChart,
  Rectangle,
  ReferenceLine,
  XAxis,
  YAxis,
} from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "./components/ui/chart"
// import { Separator } from "./components/ui/separator"
import { formatDate, formatPercentage } from "./utils/formatters" // Add this import
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs"
import { Slider } from "./components/ui/slider"

// Add this constant at the top of your file, outside of the App function
const DEBATE_DATE = new Date('2024-09-10').getTime()

interface SimulationResult {
  timestamp: string
  win_probabilities: {
    "Donald Trump": number
    "Kamala Harris": number
  }
}

const chartConfig = {
  "Donald Trump": {
    label: "Donald Trump",
    color: "hsl(0, 100%, 50%)", // Bright red
  },
  "Kamala Harris": {
    label: "Kamala Harris",
    color: "hsl(240, 100%, 50%)", // Bright blue
  },
}

function App() {
  const [chartData, setChartData] = useState<SimulationResult[]>([])
  const [daysToShow, setDaysToShow] = useState(30) // Default to showing this many days
  const [error, setError] = useState<string | null>(null) // Add this line

  useEffect(() => {
    fetch('./simulation_results.json')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        if (data.length === 0) {
          throw new Error('No data received');
        }
        setChartData(data);
        console.log('Data loaded:', data); // Add this line
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setError(error.message); // Add this line
      });
  }, [])

  const formattedData = useMemo(() => {
    const dailyData: { [key: string]: { sum: { [key: string]: number }, count: number } } = {}

    chartData.forEach(result => {
      const date = new Date(result.timestamp).toDateString()
      if (!dailyData[date]) {
        dailyData[date] = { sum: { "Donald Trump": 0, "Kamala Harris": 0 }, count: 0 }
      }
      dailyData[date].sum["Donald Trump"] += result.win_probabilities["Donald Trump"]
      dailyData[date].sum["Kamala Harris"] += result.win_probabilities["Kamala Harris"]
      dailyData[date].count++
    })

    return Object.entries(dailyData).map(([date, data]) => ({
      timestamp: new Date(date).getTime(),
      "Donald Trump": (data.sum["Donald Trump"] / data.count) * 100,
      "Kamala Harris": (data.sum["Kamala Harris"] / data.count) * 100,
    })).sort((a, b) => a.timestamp - b.timestamp)
  }, [chartData])

  const filteredData = useMemo(() => {
    const cutoffDate = new Date()
    cutoffDate.setDate(cutoffDate.getDate() - daysToShow)
    return formattedData.filter(data => data.timestamp >= cutoffDate.getTime())
  }, [formattedData, daysToShow])

  console.log('Formatted data:', formattedData);
  console.log('Filtered data:', filteredData);

  const renderChart = (ChartComponent: typeof BarChart | typeof LineChart) => (
    <ChartContainer config={chartConfig}>
      <ChartComponent
        width={600}
        height={300}
        margin={{
          left: 0,
          right: 0,
        }}
        data={filteredData}
      >
        {ChartComponent === LineChart && <CartesianGrid vertical={false} />}
        <XAxis
          dataKey="timestamp"
          tickLine={false}
          axisLine={false}
          tickMargin={8}
          tickFormatter={formatDate}
          domain={['dataMin', 'dataMax']}  // Add this line
          type="number"  // Add this line
        />
        {ChartComponent === LineChart && (
          <YAxis
            tickLine={false}
            axisLine={false}
            tickMargin={8}
            tickFormatter={(value) => `${value}%`}
          />
        )}
        <ChartTooltip
          content={
            <ChartTooltipContent
              indicator="dot"
              labelFormatter={(_value, payload) => {
                if (payload && payload.length > 0) {
                  return formatDate(payload[0].payload.timestamp);
                }
                return '';
              }}
              itemSorter={(a) => -(a.value ?? 0)}
              formatter={(value, name) => [
                `${formatPercentage(Number(value))}`,
                <span key={name} style={{ color: chartConfig[name as keyof typeof chartConfig].color }}>
                  {chartConfig[name as keyof typeof chartConfig].label}
                </span>
              ]}
            />
          }
          cursor={ChartComponent === BarChart ? false : undefined}
        />
        {ChartComponent === BarChart ? (
          <>
            <Bar
              dataKey="Donald Trump"
              fill={chartConfig["Donald Trump"].color}
              radius={5}
              fillOpacity={0.6}
              activeBar={<Rectangle fillOpacity={0.8} />}
            />
            <Bar
              dataKey="Kamala Harris"
              fill={chartConfig["Kamala Harris"].color}
              radius={5}
              fillOpacity={0.6}
              activeBar={<Rectangle fillOpacity={0.8} />}
            />
          </>
        ) : (
          <>
            <Line
              type="monotone"
              dataKey="Donald Trump"
              stroke={chartConfig["Donald Trump"].color}
              strokeWidth={2}
              dot={false}
            />
            <Line
              type="monotone"
              dataKey="Kamala Harris"
              stroke={chartConfig["Kamala Harris"].color}
              strokeWidth={2}
              dot={false}
            />
          </>
        )}
        <ReferenceLine
          y={50}
          stroke="hsl(var(--foreground) / 0.3)"
          strokeDasharray="3 3"
          strokeWidth={2}
        >
          <Label
            position="insideBottomLeft"
            value="50% Threshold"
            offset={10}
            fill="hsl(var(--foreground) / 0.5)"
          />
        </ReferenceLine>
        
        {/* Add this ReferenceLine for the debate */}
        <ReferenceLine
          x={DEBATE_DATE}
          stroke="hsl(var(--foreground) / 0.3)"
          strokeDasharray="10 5"
          strokeWidth={2}
        >
          <Label
            position="top"
            value="Kamala-Trump Debate"
            offset={-100}
            fill="hsl(var(--foreground) / 0.8)"
            angle={-90}
          />
        </ReferenceLine>
      </ChartComponent>
    </ChartContainer>
  )

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-4xl px-4 sm:px-6 lg:px-8">
        <Card className="w-full max-w-2xl mx-auto">
          <CardHeader className="space-y-0 pb-2">
            <CardDescription>Election Simulation</CardDescription>
            <CardTitle className="text-4xl tabular-nums">
              Win Probabilities
            </CardTitle>
          </CardHeader>
          <CardContent>
            {error ? (
              <div className="text-red-500">Error: {error}</div>
            ) : filteredData.length === 0 ? (
              <div>No data available</div>
            ) : (
              <>
                <Tabs defaultValue="bar">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="bar">Bar Chart</TabsTrigger>
                    <TabsTrigger value="line">Line Chart</TabsTrigger>
                  </TabsList>
                  <TabsContent value="bar">
                    {renderChart(BarChart)}
                  </TabsContent>
                  <TabsContent value="line">
                    {renderChart(LineChart)}
                  </TabsContent>
                </Tabs>
                <div className="mt-4 flex flex-col items-center">
                  <label htmlFor="days-slider" className="block text-sm font-medium text-gray-700 mb-2">
                    Days to show: {daysToShow}
                  </label>
                  <div className="w-64">
                    <Slider
                      id="days-slider"
                      min={5}
                      max={formattedData.length}
                      step={1}
                      value={[daysToShow]}
                      onValueChange={(value) => setDaysToShow(value[0])}
                    />
                  </div>
                </div>
              </>
            )}
          </CardContent>
          <CardFooter className="flex-col items-start gap-1">
            <CardDescription>
              This chart shows the average daily win probabilities for Donald Trump and Kamala Harris over the last {daysToShow} days.
            </CardDescription>
          </CardFooter>
        </Card>
      </div>
    </div>
  )
}

export default App