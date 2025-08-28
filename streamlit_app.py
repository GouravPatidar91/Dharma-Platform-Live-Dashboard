#!/usr/bin/env python3
"""
Project Dharma - Streamlit Cloud Demo Version
Simplified version for online deployment and hackathon demo
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time

# Page configuration
st.set_page_config(
    page_title="Project Dharma - AI Social Media Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .alert-high { background-color: #ff4444; }
    .alert-medium { background-color: #ffaa00; }
    .alert-low { background-color: #00aa44; }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2C3E50, #34495E);
    }
</style>
""", unsafe_allow_html=True)

def generate_sample_data():
    """Generate sample data for demo purposes"""
    np.random.seed(42)
    
    # Sample social media posts
    platforms = ['Twitter', 'YouTube', 'TikTok', 'Telegram', 'Facebook']
    sentiments = ['Pro-India', 'Neutral', 'Anti-India']
    
    posts_data = []
    for i in range(100):
        post = {
            'id': f'post_{i}',
            'platform': np.random.choice(platforms),
            'content': f'Sample social media content {i}',
            'sentiment': np.random.choice(sentiments, p=[0.4, 0.4, 0.2]),
            'bot_probability': np.random.random(),
            'engagement': np.random.randint(10, 10000),
            'timestamp': datetime.now() - timedelta(hours=np.random.randint(0, 168)),
            'language': np.random.choice(['Hindi', 'English', 'Bengali', 'Tamil']),
            'risk_score': np.random.random()
        }
        posts_data.append(post)
    
    return pd.DataFrame(posts_data)

def generate_campaign_data():
    """Generate sample campaign data"""
    campaigns = [
        {
            'id': 'camp_001',
            'name': 'Coordinated Disinformation Campaign #1',
            'status': 'Active',
            'severity': 'High',
            'posts_count': 156,
            'accounts_involved': 23,
            'platforms': ['Twitter', 'YouTube'],
            'start_date': datetime.now() - timedelta(days=3),
            'confidence': 0.87
        },
        {
            'id': 'camp_002', 
            'name': 'Bot Network Activity',
            'status': 'Monitoring',
            'severity': 'Medium',
            'posts_count': 89,
            'accounts_involved': 12,
            'platforms': ['TikTok', 'Telegram'],
            'start_date': datetime.now() - timedelta(days=1),
            'confidence': 0.72
        }
    ]
    return campaigns

def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🛡️ PROJECT DHARMA</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Social Media Intelligence Platform</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🔧 Control Panel")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["🏠 Dashboard Overview", "📊 Campaign Analysis", "🚨 Alert Management", "🤖 AI Analysis", "📈 System Metrics"]
    )
    
    # Generate sample data
    posts_df = generate_sample_data()
    campaigns = generate_campaign_data()
    
    if page == "🏠 Dashboard Overview":
        show_dashboard_overview(posts_df, campaigns)
    elif page == "📊 Campaign Analysis":
        show_campaign_analysis(posts_df, campaigns)
    elif page == "🚨 Alert Management":
        show_alert_management()
    elif page == "🤖 AI Analysis":
        show_ai_analysis(posts_df)
    elif page == "📈 System Metrics":
        show_system_metrics()

def show_dashboard_overview(posts_df, campaigns):
    """Dashboard overview page"""
    st.header("📊 Real-time Intelligence Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Posts Monitored", "125,847", "↗️ +2,341")
    with col2:
        st.metric("Active Campaigns", len([c for c in campaigns if c['status'] == 'Active']), "↗️ +1")
    with col3:
        st.metric("Bot Detection Rate", "23.4%", "↘️ -1.2%")
    with col4:
        st.metric("Threat Level", "MEDIUM", "→ Stable")
    
    # Real-time activity
    st.subheader("🔴 Live Activity Feed")
    
    # Platform distribution
    col1, col2 = st.columns(2)
    
    with col1:
        platform_counts = posts_df['platform'].value_counts()
        fig_platform = px.pie(
            values=platform_counts.values,
            names=platform_counts.index,
            title="Posts by Platform (Last 24h)"
        )
        st.plotly_chart(fig_platform, use_container_width=True)
    
    with col2:
        sentiment_counts = posts_df['sentiment'].value_counts()
        fig_sentiment = px.bar(
            x=sentiment_counts.index,
            y=sentiment_counts.values,
            title="Sentiment Distribution",
            color=sentiment_counts.values,
            color_continuous_scale="RdYlGn"
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    # Timeline
    st.subheader("📈 Activity Timeline")
    posts_df['hour'] = posts_df['timestamp'].dt.hour
    hourly_activity = posts_df.groupby('hour').size().reset_index(name='posts')
    
    fig_timeline = px.line(
        hourly_activity,
        x='hour',
        y='posts',
        title="Hourly Post Activity",
        markers=True
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Recent alerts
    st.subheader("🚨 Recent Alerts")
    alerts = [
        {"time": "2 min ago", "type": "High Risk", "message": "Coordinated bot activity detected on Twitter"},
        {"time": "15 min ago", "type": "Medium Risk", "message": "Unusual engagement pattern on YouTube"},
        {"time": "1 hour ago", "type": "Low Risk", "message": "New disinformation narrative identified"}
    ]
    
    for alert in alerts:
        alert_class = f"alert-{alert['type'].split()[0].lower()}"
        st.markdown(f"""
        <div class="{alert_class}" style="padding: 10px; margin: 5px 0; border-radius: 5px; color: white;">
            <strong>{alert['time']}</strong> - {alert['type']}: {alert['message']}
        </div>
        """, unsafe_allow_html=True)

def show_campaign_analysis(posts_df, campaigns):
    """Campaign analysis page"""
    st.header("🎯 Campaign Detection & Analysis")
    
    # Campaign overview
    st.subheader("🔍 Detected Campaigns")
    
    for campaign in campaigns:
        with st.expander(f"📋 {campaign['name']} - {campaign['severity']} Priority"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Posts Involved", campaign['posts_count'])
                st.metric("Accounts", campaign['accounts_involved'])
            
            with col2:
                st.metric("Confidence Score", f"{campaign['confidence']:.2%}")
                st.metric("Duration", f"{(datetime.now() - campaign['start_date']).days} days")
            
            with col3:
                st.write("**Platforms:**")
                for platform in campaign['platforms']:
                    st.write(f"• {platform}")
                
                st.write(f"**Status:** {campaign['status']}")
    
    # Network analysis
    st.subheader("🕸️ Network Analysis")
    
    # Generate sample network data
    import networkx as nx
    
    G = nx.random_geometric_graph(20, 0.3)
    pos = nx.spring_layout(G)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    
    fig_network = go.Figure()
    
    # Add edges
    fig_network.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    ))
    
    # Add nodes
    fig_network.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=[f'Account {i}' for i in G.nodes()],
        marker=dict(
            size=10,
            color=np.random.choice(['red', 'orange', 'green'], len(G.nodes())),
            line=dict(width=2)
        )
    ))
    
    fig_network.update_layout(
        title="Account Interaction Network",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        annotations=[ dict(
            text="Red: Suspicious accounts, Orange: Monitoring, Green: Normal",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.005, y=-0.002,
            xanchor='left', yanchor='bottom',
            font=dict(size=12)
        )],
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    st.plotly_chart(fig_network, use_container_width=True)

def show_alert_management():
    """Alert management page"""
    st.header("🚨 Alert Management System")
    
    # Alert configuration
    st.subheader("⚙️ Alert Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Notification Channels:**")
        email_alerts = st.checkbox("📧 Email Notifications", value=True)
        sms_alerts = st.checkbox("📱 SMS Alerts", value=True)
        dashboard_alerts = st.checkbox("🖥️ Dashboard Notifications", value=True)
        webhook_alerts = st.checkbox("🔗 Webhook Integration", value=False)
    
    with col2:
        st.write("**Alert Thresholds:**")
        bot_threshold = st.slider("Bot Detection Threshold", 0.0, 1.0, 0.7)
        sentiment_threshold = st.slider("Sentiment Risk Threshold", 0.0, 1.0, 0.8)
        engagement_threshold = st.number_input("Unusual Engagement Threshold", value=1000)
    
    # Active alerts
    st.subheader("📋 Active Alerts")
    
    alerts_data = [
        {"ID": "ALT001", "Type": "Bot Network", "Severity": "High", "Platform": "Twitter", "Status": "Active", "Created": "2024-01-15 14:30"},
        {"ID": "ALT002", "Type": "Sentiment Anomaly", "Severity": "Medium", "Platform": "YouTube", "Status": "Investigating", "Created": "2024-01-15 13:45"},
        {"ID": "ALT003", "Type": "Coordinated Campaign", "Severity": "High", "Platform": "TikTok", "Status": "Resolved", "Created": "2024-01-15 12:15"},
    ]
    
    alerts_df = pd.DataFrame(alerts_data)
    st.dataframe(alerts_df, use_container_width=True)
    
    # Alert actions
    st.subheader("🎯 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Investigate Selected"):
            st.success("Investigation started for selected alerts")
    
    with col2:
        if st.button("✅ Mark Resolved"):
            st.success("Selected alerts marked as resolved")
    
    with col3:
        if st.button("📊 Generate Report"):
            st.success("Alert report generated and sent")
    
    with col4:
        if st.button("🚨 Escalate"):
            st.warning("Alerts escalated to senior analysts")

def show_ai_analysis(posts_df):
    """AI analysis page"""
    st.header("🤖 AI Analysis Engine")
    
    # Model performance
    st.subheader("📈 Model Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Sentiment Analysis Accuracy", "94.2%", "↗️ +0.8%")
        st.metric("Bot Detection Precision", "91.7%", "↗️ +1.2%")
    
    with col2:
        st.metric("Campaign Detection Recall", "88.9%", "↘️ -0.3%")
        st.metric("False Positive Rate", "2.1%", "↘️ -0.5%")
    
    with col3:
        st.metric("Processing Speed", "1,247 posts/min", "↗️ +156")
        st.metric("Model Confidence", "87.3%", "→ Stable")
    
    # Language analysis
    st.subheader("🌐 Multi-language Analysis")
    
    language_data = posts_df['language'].value_counts()
    fig_lang = px.bar(
        x=language_data.index,
        y=language_data.values,
        title="Posts by Language",
        color=language_data.values,
        color_continuous_scale="viridis"
    )
    st.plotly_chart(fig_lang, use_container_width=True)
    
    # Real-time analysis
    st.subheader("⚡ Real-time Analysis Demo")
    
    sample_text = st.text_area(
        "Enter text for analysis:",
        "भारत एक महान देश है और हमें इस पर गर्व होना चाहिए।"
    )
    
    if st.button("🔍 Analyze Text"):
        with st.spinner("Analyzing..."):
            time.sleep(2)  # Simulate processing
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Analysis Results:**")
                st.write(f"• **Language:** Hindi")
                st.write(f"• **Sentiment:** Pro-India (92.3% confidence)")
                st.write(f"• **Bot Probability:** 12.4% (Human-like)")
                st.write(f"• **Risk Score:** Low (0.18)")
            
            with col2:
                st.write("**Translation:**")
                st.write("India is a great country and we should be proud of it.")
                
                st.write("**Key Topics:**")
                st.write("• National Pride")
                st.write("• Patriotism")
                st.write("• Cultural Identity")

def show_system_metrics():
    """System metrics page"""
    st.header("📊 System Performance Metrics")
    
    # System health
    st.subheader("💚 System Health")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("API Gateway", "✅ Healthy", "99.9% uptime")
    with col2:
        st.metric("Database", "✅ Healthy", "< 50ms latency")
    with col3:
        st.metric("AI Services", "✅ Healthy", "1.2k req/min")
    with col4:
        st.metric("Message Queue", "✅ Healthy", "0 backlog")
    
    # Performance charts
    st.subheader("📈 Performance Trends")
    
    # Generate sample performance data
    dates = pd.date_range(start='2024-01-01', end='2024-01-15', freq='H')
    performance_data = pd.DataFrame({
        'timestamp': dates,
        'cpu_usage': np.random.normal(45, 10, len(dates)),
        'memory_usage': np.random.normal(60, 15, len(dates)),
        'response_time': np.random.normal(150, 30, len(dates)),
        'throughput': np.random.normal(1200, 200, len(dates))
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_cpu = px.line(
            performance_data,
            x='timestamp',
            y='cpu_usage',
            title='CPU Usage (%)',
            range_y=[0, 100]
        )
        st.plotly_chart(fig_cpu, use_container_width=True)
        
        fig_response = px.line(
            performance_data,
            x='timestamp',
            y='response_time',
            title='Response Time (ms)'
        )
        st.plotly_chart(fig_response, use_container_width=True)
    
    with col2:
        fig_memory = px.line(
            performance_data,
            x='timestamp',
            y='memory_usage',
            title='Memory Usage (%)',
            range_y=[0, 100]
        )
        st.plotly_chart(fig_memory, use_container_width=True)
        
        fig_throughput = px.line(
            performance_data,
            x='timestamp',
            y='throughput',
            title='Throughput (req/min)'
        )
        st.plotly_chart(fig_throughput, use_container_width=True)
    
    # Service status
    st.subheader("🔧 Service Status")
    
    services_status = [
        {"Service": "Data Collection", "Status": "🟢 Running", "Uptime": "99.8%", "Last Restart": "3 days ago"},
        {"Service": "AI Analysis", "Status": "🟢 Running", "Uptime": "99.9%", "Last Restart": "1 week ago"},
        {"Service": "Alert Management", "Status": "🟢 Running", "Uptime": "100%", "Last Restart": "2 weeks ago"},
        {"Service": "Dashboard", "Status": "🟢 Running", "Uptime": "99.7%", "Last Restart": "1 day ago"},
        {"Service": "API Gateway", "Status": "🟢 Running", "Uptime": "99.9%", "Last Restart": "5 days ago"},
    ]
    
    services_df = pd.DataFrame(services_status)
    st.dataframe(services_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><strong>Project Dharma</strong> - AI-Powered Social Media Intelligence Platform</p>
    <p>🛡️ Protecting Digital Democracy | 🤖 Powered by Advanced AI | 🌐 Multi-language Support</p>
    <p><em>Hackathon Demo Version - Full system available on GitHub</em></p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()