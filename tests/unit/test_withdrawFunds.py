from brownie import accounts, reverts


def test_withdraw(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    etherWallet.withdraw(sendAmount, {"from": etherWallet.owner()})

    assert accounts[0].balance() == accountInitBalance
    assert etherWallet.balance() == 0


def test_withdraw_notOwner(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    with reverts():
        etherWallet.withdraw(sendAmount, {"from": accounts[1]})

    assert accounts[0].balance() == accountInitBalance - sendAmount
    assert etherWallet.balance() == sendAmount


def test_withdraw_moreThanInContract(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    with reverts():
        etherWallet.withdraw("2 ether", {"from": etherWallet.owner()})

    assert accounts[0].balance() == accountInitBalance - sendAmount
    assert etherWallet.balance() == sendAmount


def test_withdraw_emptyContract(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    with reverts():
        etherWallet.withdraw(sendAmount, {"from": etherWallet.owner()})

    assert accounts[0].balance() == accountInitBalance
    assert etherWallet.balance() == 0


def test_withdraw_eventEmitted(etherWallet):
    accountInitBalance = accounts[0].balance()
    sendAmount = "1 ether"
    accounts[0].transfer(etherWallet.address, sendAmount)
    tx = etherWallet.withdraw(sendAmount, {"from": etherWallet.owner()})

    assert "EtherWithdrawn" in tx.events
