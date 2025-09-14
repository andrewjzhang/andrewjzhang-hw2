import pytest
import json
from api.index import app, text_to_number, number_to_text, base64_to_number, number_to_base64

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestTextToNumber:
    """Test text to number conversion"""
    
    def test_basic_numbers(self):
        """Test basic single digit numbers"""
        assert text_to_number("one") == 1
        assert text_to_number("two") == 2
        assert text_to_number("three") == 3
        assert text_to_number("four") == 4
        assert text_to_number("five") == 5
        assert text_to_number("six") == 6
        assert text_to_number("seven") == 7
        assert text_to_number("eight") == 8
        assert text_to_number("nine") == 9
        assert text_to_number("ten") == 10
    
    def test_zero(self):
        """Test zero conversion"""
        assert text_to_number("zero") == 0
        assert text_to_number("nil") == 0
    
    def test_case_insensitive(self):
        """Test case insensitive conversion"""
        assert text_to_number("ONE") == 1
        assert text_to_number("Two") == 2
        assert text_to_number("THREE") == 3
    
    def test_with_punctuation(self):
        """Test text with punctuation"""
        assert text_to_number("one!") == 1
        assert text_to_number("two.") == 2
        assert text_to_number("three,") == 3
    
    def test_with_and_word(self):
        """Test text with 'and' word"""
        assert text_to_number("one hundred and twenty-three") == 123
        assert text_to_number("five hundred and twenty-three") == 523
        assert text_to_number("two thousand and five") == 2005
    
    def test_invalid_text(self):
        """Test invalid text inputs"""
        with pytest.raises(ValueError):
            text_to_number("eleven")
        with pytest.raises(ValueError):
            text_to_number("twenty")
        with pytest.raises(ValueError):
            text_to_number("hundred")
        with pytest.raises(ValueError):
            text_to_number("invalid")
        with pytest.raises(ValueError):
            text_to_number("")

class TestNumberToText:
    """Test number to text conversion"""
    
    def test_basic_numbers(self):
        """Test basic number to text conversion"""
        assert number_to_text(0) == "zero"
        assert number_to_text(1) == "one"
        assert number_to_text(2) == "two"
        assert number_to_text(10) == "ten"
        assert number_to_text(42) == "forty-two"
        assert number_to_text(123) == "one hundred and twenty-three"
    
    def test_negative_numbers(self):
        """Test negative numbers"""
        assert number_to_text(-1) == "minus one"
        assert number_to_text(-42) == "minus forty-two"

class TestBase64Conversion:
    """Test base64 conversion functions"""
    
    def test_number_to_base64(self):
        """Test converting numbers to base64"""
        # Test small numbers
        assert number_to_base64(0) == "AA=="  # 0 in base64
        assert number_to_base64(1) == "AQ=="  # 1 in base64
        assert number_to_base64(42) == "Kg=="  # 42 in base64
    
    def test_base64_to_number(self):
        """Test converting base64 to numbers"""
        assert base64_to_number("AA==") == 0
        assert base64_to_number("AQ==") == 1
        assert base64_to_number("Kg==") == 42
    
    def test_base64_roundtrip(self):
        """Test base64 roundtrip conversion"""
        numbers = [0, 1, 42, 123, 255, 256, 1000]
        for num in numbers:
            b64 = number_to_base64(num)
            assert base64_to_number(b64) == num
    
    def test_invalid_base64(self):
        """Test invalid base64 inputs"""
        with pytest.raises(ValueError):
            base64_to_number("invalid!")
        with pytest.raises(ValueError):
            base64_to_number("not_base64")

class TestWebInterface:
    """Test the web interface endpoints"""
    
    def test_index_route(self, client):
        """Test the index route returns HTML"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Numeric Converter' in response.data
    
    def test_decimal_to_binary(self, client):
        """Test decimal to binary conversion"""
        response = client.post('/convert', 
            json={'input': '42', 'inputType': 'decimal', 'outputType': 'binary'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '101010'
        assert data['error'] is None
    
    def test_binary_to_decimal(self, client):
        """Test binary to decimal conversion"""
        response = client.post('/convert',
            json={'input': '101010', 'inputType': 'binary', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '42'
        assert data['error'] is None
    
    def test_decimal_to_octal(self, client):
        """Test decimal to octal conversion"""
        response = client.post('/convert',
            json={'input': '42', 'inputType': 'decimal', 'outputType': 'octal'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '52'
        assert data['error'] is None
    
    def test_octal_to_decimal(self, client):
        """Test octal to decimal conversion"""
        response = client.post('/convert',
            json={'input': '52', 'inputType': 'octal', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '42'
        assert data['error'] is None
    
    def test_decimal_to_hexadecimal(self, client):
        """Test decimal to hexadecimal conversion"""
        response = client.post('/convert',
            json={'input': '42', 'inputType': 'decimal', 'outputType': 'hexadecimal'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '2a'
        assert data['error'] is None
    
    def test_hexadecimal_to_decimal(self, client):
        """Test hexadecimal to decimal conversion"""
        response = client.post('/convert',
            json={'input': '2a', 'inputType': 'hexadecimal', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '42'
        assert data['error'] is None
    
    def test_text_to_decimal(self, client):
        """Test text to decimal conversion"""
        response = client.post('/convert',
            json={'input': 'forty two', 'inputType': 'text', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = json.loads(response.data)
        # This should fail with current implementation - "forty two" is not supported
        assert data['error'] is not None
    
    def test_decimal_to_text(self, client):
        """Test decimal to text conversion"""
        response = client.post('/convert',
            json={'input': '42', 'inputType': 'decimal', 'outputType': 'text'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 'forty-two'
        assert data['error'] is None
    
    def test_base64_to_decimal(self, client):
        """Test base64 to decimal conversion"""
        response = client.post('/convert',
            json={'input': 'Kg==', 'inputType': 'base64', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '42'
        assert data['error'] is None
    
    def test_decimal_to_base64(self, client):
        """Test decimal to base64 conversion"""
        response = client.post('/convert',
            json={'input': '42', 'inputType': 'decimal', 'outputType': 'base64'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 'Kg=='
        assert data['error'] is None
    
    def test_all_format_combinations(self, client):
        """Test conversion between all format combinations"""
        formats = ['binary', 'octal', 'decimal', 'hexadecimal', 'base64']
        test_value = '42'  # decimal representation
        expected_values = {
            'binary': '101010',
            'octal': '52', 
            'decimal': '42',
            'hexadecimal': '2a',
            'base64': 'Kg=='
        }
        
        for input_format in formats:
            for output_format in formats:
                input_val = expected_values[input_format]
                expected_output = expected_values[output_format]
                
                response = client.post('/convert',
                    json={'input': input_val, 'inputType': input_format, 'outputType': output_format})
                assert response.status_code == 200
                data = json.loads(response.data)
                assert data['result'] == expected_output, f"Failed {input_format} to {output_format}: got {data['result']}, expected {expected_output}"
                assert data['error'] is None
    
    def test_zero_conversions(self, client):
        """Test zero in all formats"""
        zero_values = {
            'binary': '0',
            'octal': '0',
            'decimal': '0', 
            'hexadecimal': '0',
            'base64': 'AA==',
            'text': 'zero'
        }
        
        for input_format, input_val in zero_values.items():
            for output_format, expected_val in zero_values.items():
                response = client.post('/convert',
                    json={'input': input_val, 'inputType': input_format, 'outputType': output_format})
                assert response.status_code == 200
                data = json.loads(response.data)
                if data['error'] is None:
                    assert data['result'] == expected_val, f"Failed {input_format} to {output_format}: got {data['result']}, expected {expected_val}"
    
    def test_readme_examples(self, client):
        """Test examples from README.md"""
        # Convert decimal to binary: Input "42" with input type "decimal" and output type "binary"
        response = client.post('/convert',
            json={'input': '42', 'inputType': 'decimal', 'outputType': 'binary'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '101010'
        assert data['error'] is None
        
        # Convert text to decimal: Input "forty two" with input type "text" and output type "decimal"
        response = client.post('/convert',
            json={'input': 'forty two', 'inputType': 'text', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '42'
        assert data['error'] is None
        
        # Convert hexadecimal to text: Input "2a" with input type "hexadecimal" and output type "text"
        response = client.post('/convert',
            json={'input': '2a', 'inputType': 'hexadecimal', 'outputType': 'text'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 'forty-two'
        assert data['error'] is None
    
    def test_error_handling(self, client):
        """Test various error conditions"""
        # Invalid binary
        response = client.post('/convert',
            json={'input': '102', 'inputType': 'binary', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['error'] is not None
        
        # Invalid octal
        response = client.post('/convert',
            json={'input': '89', 'inputType': 'octal', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['error'] is not None
        
        # Invalid hexadecimal
        response = client.post('/convert',
            json={'input': 'xyz', 'inputType': 'hexadecimal', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['error'] is not None
        
        # Invalid base64
        response = client.post('/convert',
            json={'input': 'invalid!', 'inputType': 'base64', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['error'] is not None
        
        # Invalid text
        response = client.post('/convert',
            json={'input': 'invalid text', 'inputType': 'text', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['error'] is not None
    
    def test_negative_numbers(self, client):
        """Test negative number handling"""
        # Negative decimal to text
        response = client.post('/convert',
            json={'input': '-42', 'inputType': 'decimal', 'outputType': 'text'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 'minus forty-two'
        assert data['error'] is None
        
        # Negative numbers should not work for binary/octal/hex in Python's int() function
        # but let's test the behavior
        response = client.post('/convert',
            json={'input': '-42', 'inputType': 'decimal', 'outputType': 'binary'})
        assert response.status_code == 200
        data = json.loads(response.data)
        # Python's bin() handles negative numbers with '-0b' prefix
        # but our code strips the '0b', so we get '-101010'
        assert data['result'] == '-101010'
        assert data['error'] is None

class TestBase64ByteOrder:
    """Test base64 byte order - should be little-endian according to requirements"""
    
    def test_base64_little_endian(self):
        """Test that base64 uses little-endian byte order"""
        # Test with a multi-byte number to see byte order
        number = 0x1234  # 4660 in decimal
        b64 = number_to_base64(number)
        decoded = base64_to_number(b64)
        assert decoded == number  # This should pass regardless of byte order
        
        # But let's test the actual byte representation
        import base64
        # In little-endian, 0x1234 should be stored as [0x34, 0x12]
        expected_little_endian = base64.b64encode(bytes([0x34, 0x12])).decode('utf-8')
        actual = number_to_base64(0x1234)
        
        # This should now pass with little-endian implementation
        assert actual == expected_little_endian