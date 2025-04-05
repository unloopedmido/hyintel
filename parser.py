import base64
import gzip
import io
import json
import nbtlib

def parse_item_bytes(bytes_str: str):
    """Parse base64 encoded, gzipped NBT data and return as JSON"""
    try:
        # Decode base64 and decompress gzip
        compressed_data = base64.b64decode(bytes_str)
        compressed_stream = io.BytesIO(compressed_data)
        
        with gzip.GzipFile(fileobj=compressed_stream, mode='rb') as f:
            decompressed_data = f.read()
        
        # Parse NBT data
        nbt_data = nbtlib.File.parse(io.BytesIO(decompressed_data))
        
        # Convert to a regular Python dict and then to JSON
        # Use the .json-compatible dict conversion
        item_dict = nbt_data.unpack()
        
        # Return formatted JSON
        return json.dumps(item_dict, indent=2)
    
    except nbtlib.CastError as e:
        # If NBT parsing fails, try to handle as regular data
        try:
            # Try to decode as text and convert to JSON if possible
            text = decompressed_data.decode('utf-8')
            return json.dumps({"raw_text": text}, indent=2)
        except Exception as e:
            # Fall back to hexadecimal representation
            hex_repr = decompressed_data.hex()
            return json.dumps({
                "error": str(e),
                "hex_data": hex_repr[:200] + "..." if len(hex_repr) > 200 else hex_repr
            }, indent=2)