from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_annual_route_inventory_covers_2012_to_2017() -> None:
    payload = load_yaml("data/historical-route/stage5bf-annual-route-inventory.yaml")

    assert list(payload["years"]) == ["2012", "2013", "2014", "2015", "2016", "2017"]
    assert payload["years"]["2014"]["route_directory_present"] is True
    assert payload["years"]["2014"]["signed_message_candidates"] > 0
    assert payload["years"]["2014"]["audio_video_artifacts"] > 0
