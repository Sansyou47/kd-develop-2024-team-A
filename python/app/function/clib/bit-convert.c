#include <stdio.h>
#include <stdlib.h>
#include <jpeglib.h>

void convert_bit_depth(char *input_filename, char *output_filename)
{
    struct jpeg_decompress_struct cinfo;
    struct jpeg_error_mgr jerr;
    FILE *input_file = fopen(input_filename, "rb");
    if (!input_file)
    {
        fprintf(stderr, "Cannot open %s\n", input_filename);
        return;
    }

    cinfo.err = jpeg_std_error(&jerr);
    jpeg_create_decompress(&cinfo);
    jpeg_stdio_src(&cinfo, input_file);
    jpeg_read_header(&cinfo, TRUE);
    jpeg_start_decompress(&cinfo);

    int width = cinfo.output_width;
    int height = cinfo.output_height;
    int pixel_size = cinfo.output_components;

    JSAMPARRAY buffer = (*cinfo.mem->alloc_sarray)((j_common_ptr)&cinfo, JPOOL_IMAGE, width * pixel_size, 1);

    // 出力画像データのメモリ確保（ビット深度を4ビットに下げるため、サイズを調整）
    unsigned char *output_image = malloc(width * height * pixel_size / 2);
    if (!output_image)
    {
        fprintf(stderr, "Failed to allocate memory for output image\n");
        jpeg_destroy_decompress(&cinfo);
        fclose(input_file);
        return;
    }

    unsigned char *out_ptr = output_image;
    while (cinfo.output_scanline < cinfo.output_height)
    {
        jpeg_read_scanlines(&cinfo, buffer, 1);
        for (int i = 0; i < width * pixel_size; i += 2)
        {
            // 2ピクセル分のデータを1バイトに圧縮
            *out_ptr++ = (buffer[0][i] & 0xF0) | ((buffer[0][i + 1] & 0xF0) >> 4);
        }
    }

    jpeg_finish_decompress(&cinfo);
    jpeg_destroy_decompress(&cinfo);
    fclose(input_file);

    // 変換したデータをファイルに保存
    FILE *output_file = fopen(output_filename, "wb");
    if (!output_file)
    {
        fprintf(stderr, "Cannot open %s\n", output_filename);
        free(output_image);
        return;
    }
    fwrite(output_image, 1, width * height * pixel_size / 2, output_file);
    fclose(output_file);
    free(output_image);
}

int main(int argc, char **argv)
{
    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s <input file> <output file>\n", argv[0]);
        return 1;
    }
    convert_bit_depth(argv[1], argv[2]);
    return 0;
}