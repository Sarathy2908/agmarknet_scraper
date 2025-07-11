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

### Option 1: Heroku (Recommended for beginners)

1. **Install Heroku CLI** and login:
```bash
heroku login
```

2. **Create Heroku app**:
```bash
heroku create your-app-name
```

3. **Add buildpack for Chrome**:
```bash
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome
heroku buildpacks:add heroku/python
```

4. **Deploy**:
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

5. **Open your app**:
```bash
heroku open
```

### Option 2: Railway

1. **Connect your GitHub repository** to Railway
2. **Railway will automatically detect** the Python app and deploy it
3. **Add environment variables** if needed
4. **Your app will be live** at the provided URL

### Option 3: Docker Deployment

1. **Build and run locally**:
```bash
docker-compose up --build
```

2. **Deploy to any cloud platform** that supports Docker:
   - Google Cloud Run
   - AWS ECS
   - Azure Container Instances
   - DigitalOcean App Platform

### Option 4: VPS/Server Deployment

1. **Clone the repository** on your server
2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install Chrome and ChromeDriver**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y google-chrome-stable
wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/LATEST_RELEASE/chromedriver_linux64.zip
sudo unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

4. **Run with Gunicorn**:
```bash
gunicorn --bind 0.0.0.0:5000 app:app
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
- For Docker deployment, the Dockerfile handles this automatically
- For Heroku, the buildpack handles this automatically

### CORS Issues
- The API has CORS enabled by default
- If you encounter CORS issues, check that your Flutter app is making requests to the correct URL

### Performance Issues
- The API uses headless Chrome for better performance
- Consider implementing caching for frequently requested data
- Monitor memory usage as Chrome instances consume resources

## License

This project is open source and available under the MIT License.
