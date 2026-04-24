import { AutoModel, AutoProcessor, env, RawImage } from '@huggingface/transformers';
env.backends.onnx.wasm.quantized = false;
async function main() {
    try {
        const model = await AutoModel.from_pretrained('OS-Software/InSPyReNet-SwinB-Plus-Ultra-ONNX', { quantized: false, dtype: "fp32" });
        console.log("Success");
    } catch (e) {
        console.error(e);
    }
}
main();
