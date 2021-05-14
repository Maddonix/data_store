import torch
import torchaudio

def resample(aud, newsr):
    """Resamples the audiofile to given samplerate

    Args:
        aud (tuple): tuple containing (audiodata_array, samplerate)
        newsr (int): new samplerate

    Returns:
        tuple: (audiodata_array, samplerate)
    """
    sig, sr = aud

    if sr == newsr:
        # Nothing to do
        return aud

    num_channels = sig.shape[0]
    # Resample first channel
    resig = torchaudio.transforms.Resample(sr, newsr)(sig[:1, :])
    if num_channels > 1:
        # Resample the second channel and merge both channels
        retwo = torchaudio.transforms.Resample(sr, newsr)(sig[1:, :])
        resig = torch.cat([resig, retwo])

    return (resig, newsr)