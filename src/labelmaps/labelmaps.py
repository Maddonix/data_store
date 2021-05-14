from ..labelmaps.audio_weak_labels import AudioWeakLabels
from ..labelmaps.audio_strong_labels import AudioStrongLabels

labelmaps = {
    0: AudioStrongLabels,
    1: AudioWeakLabels
}