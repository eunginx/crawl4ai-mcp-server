import asyncio
from crawl4ai import AsyncWebCrawler

async def analyze_saas_structure():
    try:
        print('🔍 Analyzing SaaS Boilerplate structure...')
        
        async with AsyncWebCrawler(verbose=True) as crawler:
            # Check the services we found earlier
            urls = [
                'https://docs.demo.saas.apptoku.com/api-reference/backend/generated/apps/finances/services/customers',
                'https://docs.demo.saas.apptoku.com/api-reference/backend/generated/apps/finances/services/subscriptions'
            ]
            
            for i, url in enumerate(urls, 1):
                print(f'\n📄 Analyzing service {i}: {url}')
                try:
                    result = await crawler.arun(
                        url=url,
                        word_count_threshold=10,
                        exclude_external_links=False,
                        process_iframes=False,
                        remove_overlay_elements=True,
                        simulate_user=False,
                        override_navigator=True
                    )
                    
                    content = result.cleaned_html
                    print(f'📊 Content length: {len(content)} characters')
                    
                    # Look for key patterns
                    if 'class' in content:
                        print('🏗️  Contains class definitions')
                    if 'def ' in content:
                        print('⚙️  Contains function definitions')
                    if 'service' in content.lower():
                        print('🔧 Service-oriented architecture')
                    if 'customer' in content.lower() or 'subscription' in content.lower():
                        print('👥 Business domain logic')
                    
                    # Show a preview
                    preview = content[:300].replace('<', '&lt;').replace('>', '&gt;')
                    print(f'📝 Preview: {preview}...')
                    
                except Exception as e:
                    print(f'❌ Error: {e}')
        
        # Provide comprehensive guide
        print('\n🎯 SaaS Boilerplate Function Creation Guide')
        print('=' * 50)
        
        print('\n1. 📁 Directory Structure:')
        print('   apps/')
        print('   ├── finances/')
        print('   │   ├── services/          ← Create functions here')
        print('   │   │   ├── customers.py')
        print('   │   │   └── subscriptions.py')
        print('   │   ├── managers/           ← Business logic')
        print('   │   └── tests/             ← Unit tests')
        print('   └── multitenancy/        ← Multi-tenant support')
        
        print('\n2. 🔧 Creating a New Function:')
        print('   Step 1: Choose the right module (e.g., finances)')
        print('   Step 2: Create service class in services/')
        print('   Step 3: Implement business methods')
        print('   Step 4: Add error handling')
        print('   Step 5: Write tests')
        print('   Step 6: Update API endpoints')
        
        print('\n3. 💻 Example Structure:')
        print('   ```python')
        print('   # apps/finances/services/my_service.py')
        print('   class MyService:')
        print('       def __init__(self):')
        print('           self.manager = SomeManager()')
        print('       ')
        print('       def create_item(self, data):')
        print('           # Validate input')
        print('           # Business logic')
        print('           # Save to database')
        print('           return result')
        print('   ```')
        
        print('\n4. 🧪 Testing:')
        print('   - Create test file in tests/')
        print('   - Use fixtures for test data')
        print('   - Test all methods')
        print('   - Mock dependencies')
        
        print('\n5. 📚 Best Practices:')
        print('   - Follow existing patterns')
        print('   - Use dependency injection')
        print('   - Handle errors gracefully')
        print('   - Add logging')
        print('   - Document your code')
        
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == "__main__":
    asyncio.run(analyze_saas_structure())
