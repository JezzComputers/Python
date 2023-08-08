function decodeUplink(input) {
var bytes = input.bytes;

var onewire_temp_data = (bytes[0] * 256 + bytes[1]);
var bat_data = (bytes[2] * 256 + bytes[3]);
var temp_data = (bytes[4] * 256 + bytes[5]);
var humid_data = (bytes[6] * 256 + bytes[7]);

  return {
    data: {
      onewire_temp:onewire_temp_data/100,
      bat:bat_data/100,
      temp:temp_data/100,
      humid:humid_data/100
    },
    warnings: [],
    errors: []
  };
}
