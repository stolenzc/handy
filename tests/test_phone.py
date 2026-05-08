from handy.commands.phone_cmd import phone_cmd


def test_valid_chinese_phone(cli):
    result = cli(phone_cmd, ["+8613800138000"])
    assert result.exit_code == 0
    assert "Valid: True" in result.output
    assert "Country: 中国" in result.output
    assert "Location: 北京" in result.output
    assert "Carrier: 中国移动" in result.output


def test_valid_chinese_phone_no_area_code(cli):
    result = cli(phone_cmd, ["13800138000"])
    assert result.exit_code == 0
    assert "Valid: True" in result.output
    assert "Country: 中国" in result.output
    assert "Location: 北京" in result.output
    assert "Carrier: 中国移动" in result.output


def test_valid_american_phone(cli):
    result = cli(phone_cmd, ["+13132361234", "-l", "en"])
    assert result.exit_code == 0
    assert "Valid: True" in result.output
    assert "Country: United States" in result.output
    assert "Location: Michigan" in result.output
    assert "Carrier:" in result.output


def test_english_echo(cli):
    result = cli(phone_cmd, ["+8613800138000", "--lang", "en"])
    assert result.exit_code == 0
    assert "Valid: True" in result.output
    assert "Country: China" in result.output
    assert "Location: Beijing" in result.output
    assert "Carrier: China Mobile" in result.output


def test_invalid_phone_number(cli):
    result = cli(phone_cmd, ["12345"])
    assert result.exit_code == 0
    assert "Valid: False" in result.output


def test_invalid_phone_malformed(cli):
    result = cli(phone_cmd, ["abc"])
    assert result.exit_code != 0


def test_lang_en(cli):
    result = cli(phone_cmd, ["+8613800138000", "--lang", "en"])
    assert result.exit_code == 0
    assert "Valid: True" in result.output


def test_lang_en_short_flag(cli):
    result = cli(phone_cmd, ["+8613800138000", "-l", "en"])
    assert result.exit_code == 0
    assert "Valid: True" in result.output


def test_lang_invalid_choice(cli):
    result = cli(phone_cmd, ["+8613800138000", "--lang", "jp"])
    assert result.exit_code != 0
