# AgMarkNet API

A Flask-based API for scraping commodity price data from AgMarkNet website. This API is designed to work seamlessly with Flutter applications.

## Features

- Web scraping of commodity prices from AgMarkNet
- RESTful API endpoints
- CORS enabled for Flutter app integration
- Production-ready with Docker support
- Multiple deployment options

## API Endpoints

### GET /
Returns API status and available endpoints

### GET /request
Get commodity price data

**Parameters:**
- `commodity` (required): Commodity name (e.g., "Tomato")
- `state` (required): State name (e.g., "Maharashtra")
- `market` (required): Market name (e.g., "Mumbai")

**Example:**
```
GET /request?commodity=Tomato&state=Maharashtra&market=Mumbai
```

### GET /health
Health check endpoint

## Deployment Options

### Option 1: Render (Recommended)

1. **Go to [render.com](https://render.com)** and sign up with GitHub
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service**:
   - **Name**: `agmarknet-api` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or choose paid if needed)
5. **Click "Create Web Service"**
6. **Your app will be live** at `https://your-app-name.onrender.com`

**Alternative: Use render.yaml (Auto-deploy)**
- Push the `render.yaml` file to your repository
- Render will automatically detect and deploy using the configuration

### Option 2: Railway

1. **Connect your GitHub repository** to Railway
2. **Railway will automatically detect** the Python app and deploy it
3. **Add environment variables** if needed
4. **Your app will be live** at the provided URL

### Option 3: Local Development

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Install Chrome and ChromeDriver** (for your OS)

3. **Run the app**:
```bash
python app.py
```

4. **Test the API**:
```bash
curl "http://localhost:5000/request?commodity=Tomato&state=Maharashtra&market=Mumbai"
```

## Flutter Integration

### 1. Add HTTP package to your Flutter app:
```yaml
dependencies:
  http: ^1.1.0
```

### 2. Create API service class:
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class AgMarkNetAPI {
  static const String baseUrl = 'https://your-api-url.herokuapp.com'; // Replace with your deployed URL
  
  static Future<Map<String, dynamic>> getCommodityData({
    required String commodity,
    required String state,
    required String market,
  }) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/request?commodity=$commodity&state=$state&market=$market'),
      );
      
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load data: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
  
  static Future<Map<String, dynamic>> getHealth() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/health'));
      return json.decode(response.body);
    } catch (e) {
      throw Exception('Health check failed: $e');
    }
  }
}
```

### 3. Use in your Flutter app:
```dart
class CommodityScreen extends StatefulWidget {
  @override
  _CommodityScreenState createState() => _CommodityScreenState();
}

class _CommodityScreenState extends State<CommodityScreen> {
  List<dynamic> commodityData = [];
  bool isLoading = false;

  Future<void> fetchData() async {
    setState(() {
      isLoading = true;
    });

    try {
      final result = await AgMarkNetAPI.getCommodityData(
        commodity: 'Tomato',
        state: 'Maharashtra',
        market: 'Mumbai',
      );
      
      setState(() {
        commodityData = result['data'] ?? [];
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Commodity Prices')),
      body: isLoading
          ? Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: commodityData.length,
              itemBuilder: (context, index) {
                final item = commodityData[index];
                return ListTile(
                  title: Text('${item['Commodity']} - ${item['City']}'),
                  subtitle: Text('Min: ₹${item['Min Prize']} | Max: ₹${item['Max Prize']}'),
                  trailing: Text('Date: ${item['Date']}'),
                );
              },
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: fetchData,
        child: Icon(Icons.refresh),
      ),
    );
  }
}
```

## Local Development

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Install Chrome and ChromeDriver** (for your OS)

3. **Run the app**:
```bash
python app.py
```

4. **Test the API**:
```bash
curl "http://localhost:5000/request?commodity=Tomato&state=Maharashtra&market=Mumbai"
```

## Environment Variables

- `PORT`: Port number (default: 5000)

## Troubleshooting

### Chrome/ChromeDriver Issues
- Ensure Chrome and ChromeDriver versions match
- For Render deployment, Chrome will be installed automatically
- For local development, install Chrome and ChromeDriver manually

### CORS Issues
- The API has CORS enabled by default
- If you encounter CORS issues, check that your Flutter app is making requests to the correct URL

### Performance Issues
- The API uses headless Chrome for better performance
- Consider implementing caching for frequently requested data
- Monitor memory usage as Chrome instances consume resources

## License

This project is open source and available under the MIT License.
