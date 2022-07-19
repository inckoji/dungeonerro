##
## Interface
##
import constInfo
import systemSetting
import wndMgr
import chat
import grp
import app
import player
import uiTaskBar
import uiCharacter
import uiInventory
import uiDragonSoul
import uisearchshop
import uiChat
import uiMessenger
import guild
import uiGift
import ui
if app.ENABLE_LSM2_NEW_STORAGE:
	import uiSpecialStorage
if app.__BL_CHEST_DROP_INFO__:
	import uiChestDropInfo
import uiHelp
import uiWhisper
import uiPointReset
import uiShop
import uiExchange
import uiSystem
import uiRestart
import uiToolTip
import uiMiniMap
import uiParty
import uiSafebox
import uiGuild
import uiQuest
import uiPrivateShopBuilder
import uiCommon
import uiRefine
import uiEquipmentDialog
import uiGameButton
import uiTip
import uiCube
import miniMap
import time
# ACCESSORY_REFINE_ADD_METIN_STONE
import uiselectitem
# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
import uiScriptLocale

import event
import localeInfo
if app.ENABLE_MELEY_LAIR_DUNGEON:
	import uidragonlairranking
if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import uiacce
if app.ENABLE_SWITCHBOT:
	import uiSwitchbot
if app.ENABLE_DUNGEON_INFO_SYSTEM:
	import uiDungeonInfo
import ui_activity_day

IsQBHide = 0
class Interface(object):
	CHARACTER_STATUS_TAB = 1
	CHARACTER_SKILL_TAB = 2

	class NewGoldChat(ui.Window):
	
		BOARD_START_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.0)
		BOARD_END_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
		BOARD_MIDDLE_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.5)
		CHAT_OUTLINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)
		
		def __init__(self, parent = None, x = 0, y = 0):
			ui.Window.__init__(self)
			self.texts = {}
			self.parent = parent
			self.SpaceBet = 14
			self.maxY = 0
			self.x = x
			self.y = y
			self.ColorValue = 0xFFffa200
			
			self.show = self.Button('Mostrar Yang', x, y+3, self.showYang, 'd:/ymir work/ui/sanyed_yang/btn_expand_normal.tga', 'd:/ymir work/ui/sanyed_yang/btn_expand_over.tga', 'd:/ymir work/ui/sanyed_yang/btn_expand_down.tga')
			self.hide = self.Button('Ocultar Yang', x, y+3, self.hideYang, 'd:/ymir work/ui/sanyed_yang/btn_minimize_normal.tga', 'd:/ymir work/ui/sanyed_yang/btn_minimize_over.tga', 'd:/ymir work/ui/sanyed_yang/btn_minimize_down.tga')
			self.show.Hide()
			self.Show()

		def Button(self, tooltipText, x, y, func, UpVisual, OverVisual, DownVisual):
			button = ui.Button()
			if self.parent != None:
				button.SetParent(self.parent)
			button.SetPosition(x, y)
			button.SetUpVisual(UpVisual)
			button.SetOverVisual(OverVisual)
			button.SetDownVisual(DownVisual)
			button.SetToolTipText(tooltipText)
			button.Show()
			button.SetEvent(func)
			return button

		def showYang(self):
			for i in xrange(len(self.texts)):
				self.texts[i].Show()
			self.hide.Show()
			self.show.Hide()
			self.Show()

		def hideYang(self):
			for i in xrange(len(self.texts)):
				self.texts[i].Hide()
			self.hide.Hide()
			self.show.Show()
			self.Hide()
			
		def GetMaxY(self):
			return self.maxY

		def AddGoldValue(self, text):
			for i in xrange(len(self.texts)):
				if len(self.texts) == 10 and i == 0:
					self.texts[i].Hide()
				x, y = self.texts[i].GetLocalPosition()
				self.texts[i].SetPosition(x, y-self.SpaceBet)

			i = 0
			if len(self.texts) == 10:
				for i in xrange(len(self.texts)-1):
					self.texts[i] = self.texts[i+1]
				i = 9
			else:
				i = len(self.texts)
			
			self.texts[i] = ui.TextLine("Tahoma:12")
			if self.parent != None:
				self.texts[i].SetParent(self.parent)
			self.texts[i].SetPosition(self.x, self.y)
			self.texts[i].SetPackedFontColor(self.ColorValue)
			self.texts[i].SetHorizontalAlignLeft()
			self.texts[i].SetOutline(TRUE)
			self.texts[i].SetText(text)
			if self.hide.IsShow():
				self.texts[i].Show()

			if self.hide.IsShow():
				x, y = self.texts[0].GetLocalPosition()
				x2, y2 = self.hide.GetLocalPosition()
				self.hide.SetPosition(x2, y-10)

		def ClearAll(self):
			self.Hide()
			self.texts = {}
			self.show.Hide()
			self.show = None
			self.hide.Hide()
			self.hide = None

		def OnRender(self):
		
			if len(self.texts) > 0 and self.hide.IsShow():
				x, y = self.hide.GetGlobalPosition()
				w, h = self.texts[0].GetTextSize()
				h = h+10
				grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.5))
				#grp.RenderBar(x, y+10, 108, h*len(self.texts)+4)
				grp.RenderGradationBar(x, y + 10, 108, h*len(self.texts)+4, self.BOARD_START_COLOR, self.BOARD_END_COLOR)
				#grp.RenderBar(x, y+h-6, 108, h*len(self.texts)+4)

	def __init__(self):
		systemSetting.SetInterfaceHandler(self)
		self.windowOpenPosition = 0
		self.dlgWhisperWithoutTarget = None
		self.inputDialog = None
		self.wndGiftBox = None
		self.tipBoard = None
		self.bigBoard = None
		self.utilizareInventar = time.clock() + 4

		# ITEM_MALL
		self.mallPageDlg = None
		# END_OF_ITEM_MALL

		self.wndWeb = None
		self.wndTaskBar = None
		self.wndCharacter = None
		self.wndInventory = None
		self.wndExpandedTaskBar = None
		self.wndDragonSoul = None
		self.wndDragonSoulRefine = None
		self.wndChat = None
		self.yangText = None
		self.wndMessenger = None
		self.wndMiniMap = None
		self.wndGuild = None
		if app.__BL_CHEST_DROP_INFO__:
			self.wndChestDropInfo = None
		self.wndGuildBuilding = None
		if app.ENABLE_LSM2_NEW_STORAGE:
			self.wndSpecialStorage = None
		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = None
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.wndDungeonInfo = None
			
		self.listGMName = {}
		self.wndQuestWindow = {}
		self.wndQuestWindowNewKey = 0
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}
		event.SetInterfaceWindow(self)

	def __del__(self):
		systemSetting.DestroyInterfaceHandler()
		event.SetInterfaceWindow(None)

	################################
	## Make Windows & Dialogs
	def __MakeUICurtain(self):
		wndUICurtain = ui.Bar("TOP_MOST")
		wndUICurtain.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		wndUICurtain.SetColor(0x77000000)
		wndUICurtain.Hide()
		self.wndUICurtain = wndUICurtain

	def __MakeMessengerWindow(self):
		self.wndMessenger = uiMessenger.MessengerWindow()

		from _weakref import proxy
		self.wndMessenger.SetWhisperButtonEvent(lambda n,i=proxy(self):i.OpenWhisperDialog(n))
		self.wndMessenger.SetGuildButtonEvent(ui.__mem_func__(self.ToggleGuildWindow))

	def __MakeGuildWindow(self):
		self.wndGuild = uiGuild.GuildWindow()

	def __MakeChatWindow(self):

		wndChat = uiChat.ChatWindow()

		wndChat.SetSize(wndChat.CHAT_WINDOW_WIDTH, 0)
		wndChat.SetPosition(wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37)
		wndChat.SetHeight(200)
		wndChat.Refresh()
		wndChat.Show()

		self.wndChat = wndChat
		self.wndChat.BindInterface(self)
		self.wndChat.SetSendWhisperEvent(ui.__mem_func__(self.OpenWhisperDialogWithoutTarget))
		self.wndChat.SetOpenChatLogEvent(ui.__mem_func__(self.ToggleChatLogWindow))

		if self.yangText:
			self.yangText.Hide()
		yangText = self.NewGoldChat(None, wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2 + -185, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37 + 9)
		self.yangText = yangText

	def OnPickMoneyNew(self, money):
		self.yangText.AddGoldValue("+%s"%(localeInfo.NumberToMoneyString(money)))

	def __MakeTaskBar(self):
		wndTaskBar = uiTaskBar.TaskBar()
		wndTaskBar.LoadWindow()
		self.wndTaskBar = wndTaskBar
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHARACTER, ui.__mem_func__(self.ToggleCharacterWindowStatusPage))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_INVENTORY, ui.__mem_func__(self.ToggleInventoryWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_MESSENGER, ui.__mem_func__(self.ToggleMessenger))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_SYSTEM, ui.__mem_func__(self.ToggleSystemDialog))
		if uiTaskBar.TaskBar.IS_EXPANDED:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND, ui.__mem_func__(self.ToggleExpandedButton))
			self.wndExpandedTaskBar = uiTaskBar.ExpandedTaskBar()
			self.wndExpandedTaskBar.LoadWindow()
			self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, ui.__mem_func__(self.ToggleDragonSoulWindow))
			self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_SEARCH_SHOP, ui.__mem_func__(self.ToggleSearchShopWindow))

		else:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHAT, ui.__mem_func__(self.ToggleChat))

		self.wndEnergyBar = None
		import uiGift
		wndGiftBox=uiGift.GiftDialog()
		wndGiftBox.Hide()
		self.wndGiftBox=wndGiftBox
		
		import app
		if app.ENABLE_ENERGY_SYSTEM:
			wndEnergyBar = uiTaskBar.EnergyBar()
			wndEnergyBar.LoadWindow()
			self.wndEnergyBar = wndEnergyBar
	
	def __OnClickGiftButton(self):
		if self.wndGameButton:
			if not self.wndGiftBox.IsShow():
				self.wndGiftBox.Open()
			else:
				self.wndGiftBox.Close()

	def ClearGift(self):
		if self.wndGameButton:
			self.wndGameButton.HideGiftButton()
		if self.wndGiftBox:
			self.wndGiftBox.Clear()
			self.wndGiftBox.Refresh()

	def __MakeParty(self):
		wndParty = uiParty.PartyWindow()
		wndParty.Hide()
		self.wndParty = wndParty

	def __MakeGameButtonWindow(self):
		wndGameButton = uiGameButton.GameButtonWindow()
		wndGameButton.SetTop()
		wndGameButton.Show()
		wndGameButton.SetButtonEvent("STATUS", ui.__mem_func__(self.__OnClickStatusPlusButton))
		wndGameButton.SetButtonEvent("SKILL", ui.__mem_func__(self.__OnClickSkillPlusButton))
		wndGameButton.SetButtonEvent("QUEST", ui.__mem_func__(self.__OnClickQuestButton))
		wndGameButton.SetButtonEvent("HELP", ui.__mem_func__(self.__OnClickHelpButton))
		wndGameButton.SetButtonEvent("BUILD", ui.__mem_func__(self.__OnClickBuildButton))
		wndGameButton.SetButtonEvent("GIFT", ui.__mem_func__(self.__OnClickGiftButton))

		self.wndGameButton = wndGameButton

	def __IsChatOpen(self):
		return True

	def __MakeWindows(self):
		wndCharacter = uiCharacter.CharacterWindow()
		wndInventory = uiInventory.InventoryWindow()
		wndInventory.BindInterfaceClass(self)
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			wndDragonSoul = uiDragonSoul.DragonSoulWindow()
			wndDragonSoulRefine = uiDragonSoul.DragonSoulRefineWindow()
		else:
			wndDragonSoul = None
			wndDragonSoulRefine = None

		wndMiniMap = uiMiniMap.MiniMap()
		wndSafebox = uiSafebox.SafeboxWindow()

		# ITEM_MALL
		wndMall = uiSafebox.MallWindow()
		self.wndMall = wndMall
		# END_OF_ITEM_MALL

		wndChatLog = uiChat.ChatLogWindow()
		wndChatLog.BindInterface(self)

		self.wndCharacter = wndCharacter
		self.wndInventory = wndInventory
		self.wndDragonSoul = wndDragonSoul
		self.wndDragonSoulRefine = wndDragonSoulRefine
		self.wndMiniMap = wndMiniMap
		self.wndSafebox = wndSafebox
		self.wndChatLog = wndChatLog
		if app.__BL_CHEST_DROP_INFO__:
			self.wndChestDropInfo = uiChestDropInfo.ChestDropInfoWindow()

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
			self.wndDragonSoulRefine.SetInventoryWindows(self.wndInventory, self.wndDragonSoul)
			self.wndInventory.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = uiSwitchbot.SwitchbotWindow()

		if app.ENABLE_LSM2_NEW_STORAGE:
			self.wndSpecialStorage = uiSpecialStorage.SpecialStorageWindow()
		else:
			self.wndSpecialStorage = None

	def __MakeDialogs(self):
		self.dlgExchange = uiExchange.ExchangeDialog()
		self.dlgExchange.LoadDialog()
		self.dlgExchange.SetCenterPosition()
		self.dlgExchange.Hide()

		self.dlgPointReset = uiPointReset.PointResetDialog()
		self.dlgPointReset.LoadDialog()
		self.dlgPointReset.Hide()

		self.dlgShop = uiShop.ShopDialog()
		self.dlgShop.LoadDialog()
		self.dlgShop.Hide()

		self.dlgRestart = uiRestart.RestartDialog()
		self.dlgRestart.LoadDialog()
		self.dlgRestart.Hide()

		self.dlgSystem = uiSystem.SystemDialog()
		self.dlgSystem.LoadDialog()
		self.dlgSystem.SetOpenHelpWindowEvent(ui.__mem_func__(self.OpenHelpWindow))

		self.dlgSystem.Hide()

		self.dlgPassword = uiSafebox.PasswordDialog()
		self.dlgPassword.Hide()

		self.hyperlinkItemTooltip = uiToolTip.HyperlinkItemToolTip()
		self.hyperlinkItemTooltip.Hide()

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()

		self.tooltipSkill = uiToolTip.SkillToolTip()
		self.tooltipSkill.Hide()

		self.privateShopBuilder = uiPrivateShopBuilder.PrivateShopBuilder()
		self.privateShopBuilder.Hide()

		self.dlgRefineNew = uiRefine.RefineDialogNew()
		self.dlgRefineNew.Hide()
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.wndDungeonInfo = uiDungeonInfo.DungeonInfo()
		else:
			self.wndDungeonInfo = None

	def __MakeHelpWindow(self):
		self.wndHelp = uiHelp.HelpWindow()
		self.wndHelp.LoadDialog()
		self.wndHelp.SetCloseEvent(ui.__mem_func__(self.CloseHelpWindow))
		self.wndHelp.Hide()

	def __MakeTipBoard(self):
		self.tipBoard = uiTip.TipBoard()
		self.tipBoard.Hide()

		self.bigBoard = uiTip.BigBoard()
		self.bigBoard.Hide()

	def __MakeWebWindow(self):
		if constInfo.IN_GAME_SHOP_ENABLE:
			import uiWeb
			self.wndWeb = uiWeb.WebWindow()
			self.wndWeb.LoadWindow()
			self.wndWeb.Hide()

	if app.ENABLE_MELEY_LAIR_DUNGEON:
		def __MakeMeleyRanking(self):
			self.wndMeleyRanking = uidragonlairranking.Window()
			self.wndMeleyRanking.LoadWindow()
			self.wndMeleyRanking.Hide()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def __MakeAcceWindow(self):
			self.wndAcceCombine = uiacce.CombineWindow()
			self.wndAcceCombine.LoadWindow()
			self.wndAcceCombine.Hide()
			
			self.wndAcceAbsorption = uiacce.AbsorbWindow()
			self.wndAcceAbsorption.LoadWindow()
			self.wndAcceAbsorption.Hide()
			
			if self.wndInventory:
				self.wndInventory.SetAcceWindow(self.wndAcceCombine, self.wndAcceAbsorption)

	def __MakeCubeWindow(self):
		self.wndCube = uiCube.CubeWindow()
		self.wndCube.LoadWindow()
		self.wndCube.Hide()

	def __MakeCubeResultWindow(self):
		self.wndCubeResult = uiCube.CubeResultWindow()
		self.wndCubeResult.LoadWindow()
		self.wndCubeResult.Hide()

	def __MakeEventWindow(self):
		self.wndCalendarEvent = ui_activity_day.EventTakvim()
		self.wndCalendarEvent.LoadWindow()
		self.wndCalendarEvent.Hide()

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def __MakeItemSelectWindow(self):
		self.wndItemSelect = uiselectitem.SelectItemWindow()
		self.wndItemSelect.Hide()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	def MakeInterface(self):
		self.__MakeMessengerWindow()
		self.__MakeGuildWindow()
		self.__MakeChatWindow()
		self.__MakeParty()
		self.__MakeWindows()
		self.__MakeDialogs()

		self.__MakeUICurtain()
		self.__MakeTaskBar()
		self.__MakeGameButtonWindow()
		self.__MakeHelpWindow()
		self.__MakeTipBoard()
		self.__MakeWebWindow()
		if app.ENABLE_MELEY_LAIR_DUNGEON:
			self.__MakeMeleyRanking()
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.__MakeAcceWindow()
		self.__MakeCubeWindow()
		self.__MakeCubeResultWindow()
		self.__MakeEventWindow()

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.__MakeItemSelectWindow()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}

		self.wndInventory.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetItemToolTip(self.tooltipItem)
			self.wndDragonSoulRefine.SetItemToolTip(self.tooltipItem)
		self.wndSafebox.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.wndAcceCombine.SetItemToolTip(self.tooltipItem)
			self.wndAcceAbsorption.SetItemToolTip(self.tooltipItem)
		self.wndCube.SetItemToolTip(self.tooltipItem)
		self.wndCubeResult.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_LSM2_NEW_STORAGE:
			self.wndSpecialStorage.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot.SetItemToolTip(self.tooltipItem)

		# ITEM_MALL
		self.wndMall.SetItemToolTip(self.tooltipItem)
		# END_OF_ITEM_MALL

		self.wndCharacter.SetSkillToolTip(self.tooltipSkill)
		self.wndTaskBar.SetItemToolTip(self.tooltipItem)
		self.wndTaskBar.SetSkillToolTip(self.tooltipSkill)
		self.wndGuild.SetSkillToolTip(self.tooltipSkill)

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.wndItemSelect.SetItemToolTip(self.tooltipItem)
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		self.dlgShop.SetItemToolTip(self.tooltipItem)
		self.dlgExchange.SetItemToolTip(self.tooltipItem)
		self.privateShopBuilder.SetItemToolTip(self.tooltipItem)

		self.__InitWhisper()
		self.DRAGON_SOUL_IS_QUALIFIED = False

	def MakeHyperlinkTooltip(self, hyperlink):
		tokens = hyperlink.split(":")
		if tokens and len(tokens):
			type = tokens[0]
			if "item" == type:
				self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)

	## Make Windows & Dialogs
	################################

	def Close(self):
		if self.dlgWhisperWithoutTarget:
			self.dlgWhisperWithoutTarget.Destroy()
			del self.dlgWhisperWithoutTarget

		if uiQuest.QuestDialog.__dict__.has_key("QuestCurtain"):
			uiQuest.QuestDialog.QuestCurtain.Close()

		if self.wndQuestWindow:
			for key, eachQuestWindow in self.wndQuestWindow.items():
				eachQuestWindow.nextCurtainMode = -1
				eachQuestWindow.CloseSelf()
				eachQuestWindow = None
		self.wndQuestWindow = {}

		if self.wndChat:
			self.wndChat.Destroy()

		if self.yangText:
			self.yangText.ClearAll()

		if self.wndTaskBar:
			self.wndTaskBar.Destroy()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Destroy()

		if self.wndEnergyBar:
			self.wndEnergyBar.Destroy()

		if self.wndCharacter:
			self.wndCharacter.Destroy()

		if self.wndInventory:
			self.wndInventory.Destroy()

		if self.wndDragonSoul:
			self.wndDragonSoul.Destroy()

		if self.wndDragonSoulRefine:
			self.wndDragonSoulRefine.Destroy()

		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Hide()
				self.wndDungeonInfo.Destroy()
				self.wndDungeonInfo = None
				del self.wndDungeonInfo

		if app.ENABLE_LSM2_NEW_STORAGE:
			if self.wndSpecialStorage:
				self.wndSpecialStorage.Destroy()

		if self.dlgExchange:
			self.dlgExchange.Destroy()

		if self.dlgPointReset:
			self.dlgPointReset.Destroy()

		if self.dlgShop:
			self.dlgShop.Destroy()

		if self.dlgRestart:
			self.dlgRestart.Destroy()

		if self.dlgSystem:
			self.dlgSystem.Destroy()

		if self.dlgPassword:
			self.dlgPassword.Destroy()

		if self.wndMiniMap:
			self.wndMiniMap.Destroy()

		if self.wndSafebox:
			self.wndSafebox.Destroy()

		if self.wndWeb:
			self.wndWeb.Destroy()
			self.wndWeb = None

		if self.wndMall:
			self.wndMall.Destroy()

		if self.wndParty:
			self.wndParty.Destroy()

		if self.wndHelp:
			self.wndHelp.Destroy()

		if self.wndGiftBox:
			self.wndGiftBox.Clear()
			self.wndGiftBox.Hide()
			self.wndGiftBox.Destroy()
		del self.wndGiftBox
		
		if app.ENABLE_MELEY_LAIR_DUNGEON:
			if self.wndMeleyRanking:
				self.wndMeleyRanking.Destroy()

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if self.wndAcceCombine:
				self.wndAcceCombine.Destroy()
			
			if self.wndAcceAbsorption:
				self.wndAcceAbsorption.Destroy()	

		if self.wndCube:
			self.wndCube.Destroy()

		if self.wndCubeResult:
			self.wndCubeResult.Destroy()

		if self.wndCalendarEvent:
			self.wndCalendarEvent.Destroy()

		if self.wndMessenger:
			self.wndMessenger.Destroy()

		if self.wndGuild:
			self.wndGuild.Destroy()

		if self.privateShopBuilder:
			self.privateShopBuilder.Destroy()

		if self.dlgRefineNew:
			self.dlgRefineNew.Destroy()

		if self.wndGuildBuilding:
			self.wndGuildBuilding.Destroy()

		if self.wndGameButton:
			self.wndGameButton.Destroy()

		if app.__BL_CHEST_DROP_INFO__:
			if self.wndChestDropInfo:
				del self.wndChestDropInfo
		# ITEM_MALL
		if self.mallPageDlg:
			self.mallPageDlg.Destroy()
		# END_OF_ITEM_MALL

		# ACCESSORY_REFINE_ADD_METIN_STONE
		if self.wndItemSelect:
			self.wndItemSelect.Destroy()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Destroy()

		self.wndChatLog.Destroy()
		for btn in self.questButtonList:
			btn.SetEvent(0)
		for btn in self.whisperButtonList:
			btn.SetEvent(0)
		for dlg in self.whisperDialogDict.itervalues():
			dlg.Destroy()
		for brd in self.guildScoreBoardDict.itervalues():
			brd.Destroy()
		for dlg in self.equipmentDialogDict.itervalues():
			dlg.Destroy()

		# ITEM_MALL
		del self.mallPageDlg
		# END_OF_ITEM_MALL

		del self.wndGuild
		del self.wndMessenger
		del self.wndUICurtain
		del self.wndChat
		del self.yangText
		del self.wndTaskBar
		if self.wndExpandedTaskBar:
			del self.wndExpandedTaskBar
		del self.wndEnergyBar
		del self.wndCharacter
		del self.wndInventory
		if self.wndDragonSoul:
			del self.wndDragonSoul
		if self.wndDragonSoulRefine:
			del self.wndDragonSoulRefine
		if app.ENABLE_LSM2_NEW_STORAGE:
			if self.wndSpecialStorage:
				del self.wndSpecialStorage
		del self.dlgExchange
		del self.dlgPointReset
		del self.dlgShop
		del self.dlgRestart
		del self.dlgSystem
		del self.dlgPassword
		del self.hyperlinkItemTooltip
		del self.tooltipItem
		del self.tooltipSkill
		del self.wndMiniMap
		del self.wndSafebox
		del self.wndMall
		del self.wndParty
		del self.wndHelp
		if app.ENABLE_MELEY_LAIR_DUNGEON:
			del self.wndMeleyRanking
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			del self.wndAcceCombine
			del self.wndAcceAbsorption
		del self.wndCube
		del self.wndCubeResult
		del self.privateShopBuilder
		del self.wndCalendarEvent
		del self.inputDialog
		del self.wndChatLog
		del self.dlgRefineNew
		del self.wndGuildBuilding
		del self.wndGameButton
		del self.tipBoard
		del self.bigBoard
		del self.wndItemSelect

		if app.ENABLE_SWITCHBOT:
			del self.wndSwitchbot	

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		uiChat.DestroyChatInputSetWindow()

	## Skill
	def OnUseSkill(self, slotIndex, coolTime):
		self.wndCharacter.OnUseSkill(slotIndex, coolTime)
		self.wndTaskBar.OnUseSkill(slotIndex, coolTime)
		self.wndGuild.OnUseSkill(slotIndex, coolTime)

	def OnActivateSkill(self, slotIndex):
		self.wndCharacter.OnActivateSkill(slotIndex)
		self.wndTaskBar.OnActivateSkill(slotIndex)

	def OnDeactivateSkill(self, slotIndex):
		self.wndCharacter.OnDeactivateSkill(slotIndex)
		self.wndTaskBar.OnDeactivateSkill(slotIndex)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.wndTaskBar.OnChangeCurrentSkill(skillSlotNumber)

	def SelectMouseButtonEvent(self, dir, event):
		self.wndTaskBar.SelectMouseButtonEvent(dir, event)

	## Refresh
	def RefreshAlignment(self):
		self.wndCharacter.RefreshAlignment()

	def RefreshStatus(self):
		self.wndTaskBar.RefreshStatus()
		self.wndCharacter.RefreshStatus()
		self.wndInventory.RefreshStatus()
		if self.wndEnergyBar:
			self.wndEnergyBar.RefreshStatus()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshStatus()

	def RefreshStamina(self):
		self.wndTaskBar.RefreshStamina()

	def RefreshSkill(self):
		self.wndCharacter.RefreshSkill()
		self.wndTaskBar.RefreshSkill()
		
	def OpenGift(self):
		if self.wndGameButton:
			self.wndGameButton.ShowGiftButton()

	def RefreshInventory(self):
		self.wndTaskBar.RefreshQuickSlot()
		self.wndInventory.RefreshItemSlot()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshItemSlot()
		if app.ENABLE_LSM2_NEW_STORAGE:
			self.wndSpecialStorage.RefreshItemSlot()

	if app.ENABLE_EXTEND_INVEN_SYSTEM:
		def SetInventoryPageKilit(self):
			if constInfo.envanter == 2:
				if player.GetExtendInventory() == 0:
					self.wndInventory.engelblack.Show()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Show()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Show()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Show()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Show()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Show()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Show()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 1:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Show()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Show()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Show()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Show()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Show()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Show()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 2:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Show()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Show()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Show()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Show()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Show()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 3:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Show()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Show()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Show()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Show()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 4:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Show()
					self.wndInventory.engelblack5cl.Hide()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Show()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Show()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 5:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Hide()
					self.wndInventory.engelblack6.Show()
					self.wndInventory.engelblack6cl.Hide()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Show()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 6:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Hide()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Hide()
					self.wndInventory.engelblack7.Show()
					self.wndInventory.engelblack7cl.Hide()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 7:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Hide()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Hide()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Hide()
					self.wndInventory.engelblack8.Show()
					self.wndInventory.engelblack8cl.Hide()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 8:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Hide()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Hide()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Hide()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Hide()
					self.wndInventory.engelblack9.Show()
					self.wndInventory.engelblack9cl.Hide()
				elif player.GetExtendInventory() == 9:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Hide()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Hide()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Hide()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Hide()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Hide()
				elif player.GetExtendInventory() >= 10:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Hide()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Hide()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Hide()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Hide()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Hide()
			elif constInfo.envanter == 3:
				if player.GetExtendInventory() >= 0 and player.GetExtendInventory() <= 8:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Show()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Show()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Show()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Show()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Show()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Show()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Show()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 9:
					self.wndInventory.engelblack.Show()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Show()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Show()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Show()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Show()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Show()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Show()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 10:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Show()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Show()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Show()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Show()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Show()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Show()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 11:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Show()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Show()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Show()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Show()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Show()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 12:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Show()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Show()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Show()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Show()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 13:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Show()
					self.wndInventory.engelblack5cl.Hide()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Show()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Show()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 14:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Hide()
					self.wndInventory.engelblack6.Show()
					self.wndInventory.engelblack6cl.Hide()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Show()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 15:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Hide()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Hide()
					self.wndInventory.engelblack7.Show()
					self.wndInventory.engelblack7cl.Hide()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Show()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 16:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Hide()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Hide()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Hide()
					self.wndInventory.engelblack8.Show()
					self.wndInventory.engelblack8cl.Hide()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Show()
				elif player.GetExtendInventory() == 17:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Hide()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Hide()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Hide()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Hide()
					self.wndInventory.engelblack9.Show()
					self.wndInventory.engelblack9cl.Hide()
				elif player.GetExtendInventory() == 18:
					self.wndInventory.engelblack.Hide()
					self.wndInventory.engelblackcl.Hide()
					self.wndInventory.engelblack2.Hide()
					self.wndInventory.engelblack2cl.Hide()
					self.wndInventory.engelblack3.Hide()
					self.wndInventory.engelblack3cl.Hide()
					self.wndInventory.engelblack4.Hide()
					self.wndInventory.engelblack4cl.Hide()
					self.wndInventory.engelblack5.Hide()
					self.wndInventory.engelblack5cl.Hide()
					self.wndInventory.engelblack6.Hide()
					self.wndInventory.engelblack6cl.Hide()
					self.wndInventory.engelblack7.Hide()
					self.wndInventory.engelblack7cl.Hide()
					self.wndInventory.engelblack8.Hide()
					self.wndInventory.engelblack8cl.Hide()
					self.wndInventory.engelblack9.Hide()
					self.wndInventory.engelblack9cl.Hide()
			else:
				self.wndInventory.engelblack.Hide()
				self.wndInventory.engelblackcl.Hide()
				self.wndInventory.engelblack2.Hide()
				self.wndInventory.engelblack2cl.Hide()
				self.wndInventory.engelblack3.Hide()
				self.wndInventory.engelblack3cl.Hide()
				self.wndInventory.engelblack4.Hide()
				self.wndInventory.engelblack4cl.Hide()
				self.wndInventory.engelblack5.Hide()
				self.wndInventory.engelblack5cl.Hide()
				self.wndInventory.engelblack6.Hide()
				self.wndInventory.engelblack6cl.Hide()
				self.wndInventory.engelblack7.Hide()
				self.wndInventory.engelblack7cl.Hide()
				self.wndInventory.engelblack8.Hide()
				self.wndInventory.engelblack8cl.Hide()
				self.wndInventory.engelblack9.Hide()
				self.wndInventory.engelblack9cl.Hide()
			self.wndInventory.RefreshBagSlotWindow()

	def RefreshCharacter(self):
		self.wndCharacter.RefreshCharacter()
		self.wndTaskBar.RefreshQuickSlot()

	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

	def RefreshSafebox(self):
		self.wndSafebox.RefreshSafebox()

	# ITEM_MALL
	def RefreshMall(self):
		self.wndMall.RefreshMall()

	def OpenItemMall(self):
		if not self.mallPageDlg:
			self.mallPageDlg = uiShop.MallPageDialog()

		self.mallPageDlg.Open()
	# END_OF_ITEM_MALL

	def RefreshMessenger(self):
		self.wndMessenger.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.wndGuild.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.wndGuild.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.wndGuild.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.wndGuild.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.wndGuild.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.wndGuild.RefreshGuildGradePage()

	def DeleteGuild(self):
		self.wndMessenger.ClearGuildMember()
		self.wndGuild.DeleteGuild()

	def RefreshMobile(self):
		self.dlgSystem.RefreshMobile()

	def OnMobileAuthority(self):
		self.dlgSystem.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.dlgSystem.OnBlockMode(mode)

	## Calling Functions
	# PointReset
	def OpenPointResetDialog(self):
		self.dlgPointReset.Show()
		self.dlgPointReset.SetTop()

	def ClosePointResetDialog(self):
		self.dlgPointReset.Close()

	# Shop
	def OpenShopDialog(self, vid):
		self.wndInventory.Show()
		self.wndInventory.SetTop()
		self.dlgShop.Open(vid)
		self.dlgShop.SetTop()

	def CloseShopDialog(self):
		self.dlgShop.Close()

	def RefreshShopDialog(self):
		self.dlgShop.Refresh()

	## Quest
	def OpenCharacterWindowQuestPage(self):
		self.wndCharacter.Show()
		self.wndCharacter.SetState("QUEST")

	def OpenQuestWindow(self, skin, idx):

		wnds = ()

		q = uiQuest.QuestDialog(skin, idx)
		q.SetWindowName("QuestWindow" + str(idx))
		q.Show()
		if skin:
			q.Lock()
			wnds = self.__HideWindows()

			# UNKNOWN_UPDATE
			q.AddOnDoneEvent(lambda tmp_self, args=wnds: self.__ShowWindows(args))
			# END_OF_UNKNOWN_UPDATE

		if skin:
			q.AddOnCloseEvent(q.Unlock)
		q.AddOnCloseEvent(lambda key = self.wndQuestWindowNewKey:ui.__mem_func__(self.RemoveQuestDialog)(key))
		self.wndQuestWindow[self.wndQuestWindowNewKey] = q

		self.wndQuestWindowNewKey = self.wndQuestWindowNewKey + 1

		# END_OF_UNKNOWN_UPDATE

	def RemoveQuestDialog(self, key):
		del self.wndQuestWindow[key]

	## Exchange
	def StartExchange(self):
		self.dlgExchange.OpenDialog()
		self.dlgExchange.Refresh()

	def EndExchange(self):
		self.dlgExchange.CloseDialog()

	def RefreshExchange(self):
		self.dlgExchange.Refresh()

	## Party
	def AddPartyMember(self, pid, name):
		self.wndParty.AddPartyMember(pid, name)

		self.__ArrangeQuestButton()

	def UpdatePartyMemberInfo(self, pid):
		self.wndParty.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.wndParty.RemovePartyMember(pid)

		##!! 20061026.levites.퀘스트_위치_보정
		self.__ArrangeQuestButton()

	def LinkPartyMember(self, pid, vid):
		self.wndParty.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.wndParty.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.wndParty.UnlinkAllPartyMember()

	def ExitParty(self):
		self.wndParty.ExitParty()

		##!! 20061026.levites.퀘스트_위치_보정
		self.__ArrangeQuestButton()

	def PartyHealReady(self):
		self.wndParty.PartyHealReady()

	def ChangePartyParameter(self, distributionMode):
		self.wndParty.ChangePartyParameter(distributionMode)

	## Safebox
	def AskSafeboxPassword(self):
		if self.wndSafebox.IsShow():
			return

		# SAFEBOX_PASSWORD
		self.dlgPassword.SetTitle(localeInfo.PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/safebox_password ")
		# END_OF_SAFEBOX_PASSWORD

		self.dlgPassword.ShowDialog()

	def OpenSafeboxWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndSafebox.ShowWindow(size)

	def RefreshSafeboxMoney(self):
		self.wndSafebox.RefreshSafeboxMoney()

	def CommandCloseSafebox(self):
		self.wndSafebox.CommandCloseSafebox()

	# ITEM_MALL
	def AskMallPassword(self):
		if self.wndMall.IsShow():
			return
		self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/mall_password ")
		self.dlgPassword.ShowDialog()

	def OpenMallWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndMall.ShowWindow(size)

	def CommandCloseMall(self):
		self.wndMall.CommandCloseMall()
	# END_OF_ITEM_MALL

	## Guild
	def OnStartGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnStartGuildWar(guildSelf, guildOpp)

		guildWarScoreBoard = uiGuild.GuildWarScoreBoard()
		guildWarScoreBoard.Open(guildSelf, guildOpp)
		guildWarScoreBoard.Show()
		self.guildScoreBoardDict[uiGuild.GetGVGKey(guildSelf, guildOpp)] = guildWarScoreBoard

	def OnEndGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnEndGuildWar(guildSelf, guildOpp)

		key = uiGuild.GetGVGKey(guildSelf, guildOpp)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].Destroy()
		del self.guildScoreBoardDict[key]

	# GUILDWAR_MEMBER_COUNT
	def UpdateMemberCount(self, gulidID1, memberCount1, guildID2, memberCount2):
		key = uiGuild.GetGVGKey(gulidID1, guildID2)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].UpdateMemberCount(gulidID1, memberCount1, guildID2, memberCount2)
	# END_OF_GUILDWAR_MEMBER_COUNT

	def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point):
		key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
		if not self.guildScoreBoardDict.has_key(key):
			return

		guildBoard = self.guildScoreBoardDict[key]
		guildBoard.SetScore(gainGuildID, opponentGuildID, point)

	## PK Mode
	def OnChangePKMode(self):
		self.wndCharacter.RefreshAlignment()
		self.dlgSystem.OnChangePKMode()

	## Refine
	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type):
		self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)

	## Show & Hide
	def ShowDefaultWindows(self):
		self.wndTaskBar.Show()
		self.wndMiniMap.Show()
		self.wndMiniMap.ShowMiniMap()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()

	def ShowAllWindows(self):
		self.wndTaskBar.Show()
		self.wndCharacter.Show()
		self.wndInventory.Show()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.Show()
			self.wndDragonSoulRefine.Show()
		self.wndChat.Show()
		self.yangText.Show()
		self.wndMiniMap.Show()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Show()
			self.wndExpandedTaskBar.SetTop()

	def HideAllWindows(self):
		if self.wndTaskBar:
			self.wndTaskBar.Hide()

		if self.wndEnergyBar:
			self.wndEnergyBar.Hide()

		if self.wndCharacter:
			self.wndCharacter.Hide()

		if self.wndInventory:
			self.wndInventory.Hide()

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.Hide()
			self.wndDragonSoulRefine.Hide()

		if self.wndChat:
			self.wndChat.Hide()

		if self.yangText:
			self.yangText.Hide()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()

		if self.wndMessenger:
			self.wndMessenger.Hide()

		if self.wndGuild:
			self.wndGuild.Hide()
				
		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()

		if app.__BL_CHEST_DROP_INFO__:
			if self.wndChestDropInfo:
				self.wndChestDropInfo.Hide()

		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Hide()

		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Hide()

	def ShowMouseImage(self):
		self.wndTaskBar.ShowMouseImage()

	def HideMouseImage(self):
		self.wndTaskBar.HideMouseImage()

	def ToggleChat(self):
		if True == self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
		else:
			# 웹페이지가 열렸을때는 채팅 입력이 안됨
			if self.wndWeb and self.wndWeb.IsShow():
				pass
			else:
				self.wndChat.OpenChat()

	def IsOpenChat(self):
		return self.wndChat.IsEditMode()

	def SetChatFocus(self):
		self.wndChat.SetChatFocus()

	def OpenRestartDialog(self):
		self.dlgRestart.OpenDialog()
		self.dlgRestart.SetTop()

	def CloseRestartDialog(self):
		self.dlgRestart.Close()

	def ToggleSystemDialog(self):
		if False == self.dlgSystem.IsShow():
			self.dlgSystem.OpenDialog()
			self.dlgSystem.SetTop()
		else:
			self.dlgSystem.Close()

	def OpenSystemDialog(self):
		self.dlgSystem.OpenDialog()
		self.dlgSystem.SetTop()

	def ToggleMessenger(self):
		if self.wndMessenger.IsShow():
			self.wndMessenger.Hide()
		else:
			self.wndMessenger.SetTop()
			self.wndMessenger.Show()

	def ToggleMiniMap(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			if False == self.wndMiniMap.isShowMiniMap():
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMap.SetTop()
			else:
				self.wndMiniMap.HideMiniMap()

		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def PressMKey(self):
		if app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
			self.ToggleMessenger()

		else:
			self.ToggleMiniMap()

	def SetMapName(self, mapName):
		self.wndMiniMap.SetMapName(mapName)

	def MiniMapScaleUp(self):
		self.wndMiniMap.ScaleUp()

	def MiniMapScaleDown(self):
		self.wndMiniMap.ScaleDown()

	def ToggleCharacterWindow(self, state):
		if False == player.IsObserverMode():
			if False == self.wndCharacter.IsShow():
				self.OpenCharacterWindowWithState(state)
			else:
				if state == self.wndCharacter.GetState():
					self.wndCharacter.OverOutItem()
					self.wndCharacter.Close()
				else:
					self.wndCharacter.SetState(state)

	def OpenCharacterWindowWithState(self, state):
		if False == player.IsObserverMode():
			self.wndCharacter.SetState(state)
			self.wndCharacter.Show()
			self.wndCharacter.SetTop()

	def ToggleCharacterWindowStatusPage(self):
		self.ToggleCharacterWindow("STATUS")

	if app.BL_KILL_BAR:
		def AddKillInfo(self, killer, victim, killer_race, victim_race, weapon_type):
			self.wndMiniMap.AddKillInfo(killer, victim, killer_race, victim_race, weapon_type)

	def ToggleInventoryWindow(self):
		if time.clock() >= self.utilizareInventar:
			if False == player.IsObserverMode():
				if False == self.wndInventory.IsShow():
					self.wndInventory.Show()
					self.wndInventory.SetTop()
				else:
					self.wndInventory.OverOutItem()
					self.wndInventory.Close()
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Va com calma, voce esta rapido demais...")
	
	def ToggleExpandedButton(self):
		if False == player.IsObserverMode():
			if False == self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Show()
				self.wndExpandedTaskBar.SetTop()
			else:
				self.wndExpandedTaskBar.Close()

	# 용혼석
	def DragonSoulActivate(self, deck):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.ActivateDragonSoulByExtern(deck)

	def DragonSoulDeactivate(self):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.DeactivateDragonSoul()

	def Highligt_Item(self, inven_type, inven_pos):
		if player.DRAGON_SOUL_INVENTORY == inven_type:
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				self.wndDragonSoul.HighlightSlot(inven_pos)

	def DragonSoulGiveQuilification(self):
		self.DRAGON_SOUL_IS_QUALIFIED = True
		self.wndExpandedTaskBar.SetToolTipText(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, uiScriptLocale.TASKBAR_DRAGON_SOUL)

	def ToggleDragonSoulWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoul.IsShow():
					if self.DRAGON_SOUL_IS_QUALIFIED:
						self.wndDragonSoul.Show()
					else:
						try:
							self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNQUALIFIED)
							self.wndPopupDialog.Open()
						except:
							self.wndPopupDialog = uiCommon.PopupDialog()
							self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNQUALIFIED)
							self.wndPopupDialog.Open()
				else:
					self.wndDragonSoul.Close()

	def ToggleSearchShopWindow(self):
		self.ss = uisearchshop.ShopSearch()
		self.ss.Show()

	def ToggleDragonSoulWindowWithNoInfo(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoul.IsShow():
					if self.DRAGON_SOUL_IS_QUALIFIED:
						self.wndDragonSoul.Show()
				else:
					self.wndDragonSoul.Close()
					
	if app.ENABLE_LSM2_NEW_STORAGE:
		def ToggleSpecialStorageWindow(self):
			if False == player.IsObserverMode():
				if False == self.wndSpecialStorage.IsShow():
					self.wndSpecialStorage.Show()
				else:
					self.wndSpecialStorage.Close()

	def FailDragonSoulRefine(self, reason, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineFail(reason, inven_type, inven_pos)

	def SucceedDragonSoulRefine(self, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineSucceed(inven_type, inven_pos)

	def OpenDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Show()
					if None != self.wndDragonSoul:
						if False == self.wndDragonSoul.IsShow():
							self.wndDragonSoul.Show()

	def CloseDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Close()

	def ToggleGuildWindow(self):
		if not self.wndGuild.IsShow():
			if self.wndGuild.CanOpen():
				self.wndGuild.Open()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GUILD_YOU_DO_NOT_JOIN)
		else:
			self.wndGuild.OverOutItem()
			self.wndGuild.Hide()

	def ToggleChatLogWindow(self):
		if self.wndChatLog.IsShow():
			self.wndChatLog.Hide()
		else:
			self.wndChatLog.Show()

	def EventCalendarGame(self):
		if self.wndCalendarEvent.IsShow():
			self.wndCalendarEvent.Hide()
		else:
			self.wndCalendarEvent.Open()

	if app.ENABLE_SWITCHBOT:
		def ToggleSwitchbotWindow(self):
			if self.wndSwitchbot.IsShow():
				self.wndSwitchbot.Close()
			else:
				self.wndSwitchbot.Open()
				
		def RefreshSwitchbotWindow(self):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotWindow()

		def RefreshSwitchbotItem(self, slot):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotItem(slot)

	def CheckGameButton(self):
		if self.wndGameButton:
			self.wndGameButton.CheckGameButton()

	def __OnClickStatusPlusButton(self):
		self.ToggleCharacterWindow("STATUS")

	def __OnClickSkillPlusButton(self):
		self.ToggleCharacterWindow("SKILL")

	def __OnClickQuestButton(self):
		self.ToggleCharacterWindow("QUEST")

	def __OnClickHelpButton(self):
		player.SetPlayTime(1)
		self.CheckGameButton()
		self.OpenHelpWindow()

	def __OnClickBuildButton(self):
		self.BUILD_OpenWindow()

	def OpenHelpWindow(self):
		self.wndUICurtain.Show()
		self.wndHelp.Open()

	def CloseHelpWindow(self):
		self.wndUICurtain.Hide()
		self.wndHelp.Close()

	def OpenWebWindow(self, url):
		self.wndWeb.Open(url)

		# 웹페이지를 열면 채팅을 닫는다
		self.wndChat.CloseChat()

	if app.ENABLE_MELEY_LAIR_DUNGEON:
		def OpenMeleyRanking(self):
			self.wndMeleyRanking.Open()

		def RankMeleyRanking(self, line, name, members, time):
			self.wndMeleyRanking.AddRank(line, name, members, time)

	# show GIFT
	def ShowGift(self):
		self.wndTaskBar.ShowGift()

	def CloseWbWindow(self):
		self.wndWeb.Close()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def ActAcce(self, iAct, bWindow):
			if iAct == 1:
				if bWindow == True:
					if not self.wndAcceCombine.IsOpened():
						self.wndAcceCombine.Open()
					
					if not self.wndInventory.IsShow():
						self.wndInventory.Show()
				else:
					if not self.wndAcceAbsorption.IsOpened():
						self.wndAcceAbsorption.Open()
					
					if not self.wndInventory.IsShow():
						self.wndInventory.Show()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 2:
				if bWindow == True:
					if self.wndAcceCombine.IsOpened():
						self.wndAcceCombine.Close()
				else:
					if self.wndAcceAbsorption.IsOpened():
						self.wndAcceAbsorption.Close()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 3 or iAct == 4:
				if bWindow == True:
					if self.wndAcceCombine.IsOpened():
						self.wndAcceCombine.Refresh(iAct)
				else:
					if self.wndAcceAbsorption.IsOpened():
						self.wndAcceAbsorption.Refresh(iAct)
				
				self.wndInventory.RefreshBagSlotWindow()

	def OpenCubeWindow(self):
		self.wndCube.Open()

		if False == self.wndInventory.IsShow():
			self.wndInventory.Show()

	def UpdateCubeInfo(self, gold, itemVnum, count):
		self.wndCube.UpdateInfo(gold, itemVnum, count)

	def CloseCubeWindow(self):
		self.wndCube.Close()

	def FailedCubeWork(self):
		self.wndCube.Refresh()

	def SucceedCubeWork(self, itemVnum, count):
		self.wndCube.Clear()

		print "?? ?? ??! [%d:%d]" % (itemVnum, count)

		if 0: # 결과 메시지 출력은 생략 한다
			self.wndCubeResult.SetPosition(*self.wndCube.GetGlobalPosition())
			self.wndCubeResult.SetCubeResultItem(itemVnum, count)
			self.wndCubeResult.Open()
			self.wndCubeResult.SetTop()

	def __HideWindows(self):
		hideWindows = self.wndTaskBar,\
						self.wndCharacter,\
						self.wndInventory,\
						self.wndMiniMap,\
						self.wndGuild,\
						self.wndMessenger,\
						self.wndChat,\
						self.yangText,\
						self.wndParty,\
						self.wndGameButton,

		if self.wndEnergyBar:
			hideWindows += self.wndEnergyBar,

		if self.wndExpandedTaskBar:
			hideWindows += self.wndExpandedTaskBar,

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			hideWindows += self.wndDragonSoul,\
						self.wndDragonSoulRefine,

		if app.ENABLE_SWITCHBOT and self.wndSwitchbot:
			hideWindows += self.wndSwitchbot,

		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				hideWindows += self.wndDungeonInfo,

		hideWindows = filter(lambda x:x.IsShow(), hideWindows)
		map(lambda x:x.Hide(), hideWindows)
		import sys

		self.HideAllQuestButton()
		self.HideAllWhisperButton()

		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()

		return hideWindows

	def __ShowWindows(self, wnds):
		import sys
		map(lambda x:x.Show(), wnds)
		global IsQBHide
		if not IsQBHide:
			self.ShowAllQuestButton()
		else:
			self.HideAllQuestButton()

		self.ShowAllWhisperButton()

	def BINARY_OpenAtlasWindow(self):
		if self.wndMiniMap:
			self.wndMiniMap.ShowAtlas()

	def BINARY_SetObserverMode(self, flag):
		self.wndGameButton.SetObserverMode(flag)

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def BINARY_OpenSelectItemWindow(self):
		self.wndItemSelect.Open()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	#####################################################################################
	### Private Shop ###

	def OpenPrivateShopInputNameDialog(self):
		#if player.IsInSafeArea():
		#	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_OPEN_PRIVATE_SHOP_IN_SAFE_AREA)
		#	return

		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
		inputDialog.SetMaxLength(32)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenPrivateShopBuilder))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog

	def ClosePrivateShopInputNameDialog(self):
		self.inputDialog = None
		return True

	def OpenPrivateShopBuilder(self):

		if not self.inputDialog:
			return True

		if not len(self.inputDialog.GetText()):
			return True

		self.privateShopBuilder.Open(self.inputDialog.GetText())
		self.ClosePrivateShopInputNameDialog()
		return True

	def AppearPrivateShop(self, vid, text):

		board = uiPrivateShopBuilder.PrivateShopAdvertisementBoard()
		board.Open(vid, text)

		self.privateShopAdvertisementBoardDict[vid] = board

	def DisappearPrivateShop(self, vid):

		if not self.privateShopAdvertisementBoardDict.has_key(vid):
			return

		del self.privateShopAdvertisementBoardDict[vid]
		uiPrivateShopBuilder.DeleteADBoard(vid)

	#####################################################################################
	### Equipment ###

	def OpenEquipmentDialog(self, vid):
		dlg = uiEquipmentDialog.EquipmentDialog()
		dlg.SetItemToolTip(self.tooltipItem)
		dlg.SetCloseEvent(ui.__mem_func__(self.CloseEquipmentDialog))
		dlg.Open(vid)

		self.equipmentDialogDict[vid] = dlg

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogSocket(slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogAttr(slotIndex, attrIndex, type, value)

	def CloseEquipmentDialog(self, vid):
		if not vid in self.equipmentDialogDict:
			return
		del self.equipmentDialogDict[vid]

	#####################################################################################

	#####################################################################################
	### Quest ###
	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

	def RecvQuest(self, index, name):
		# QUEST_LETTER_IMAGE
		self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())
		# END_OF_QUEST_LETTER_IMAGE

	def BINARY_RecvQuest(self, index, name, iconType, iconName):

		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiWhisper.WhisperButton()

		# QUEST_LETTER_IMAGE
		##!! 20061026.levites.퀘스트_이미지_교체
		import item
		if "item"==iconType:
			item.SelectItem(int(iconName))
			buttonImageFileName=item.GetIconImageFileName()
		else:
			buttonImageFileName=iconName

		if iconName and (iconType not in ("item", "file")): # type "ex" implied
			btn.SetUpVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName.replace("open", "close")))
			btn.SetOverVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
			btn.SetDownVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
		else:
			if localeInfo.IsEUROPE():
				btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
				btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
				btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
			else:
				btn.SetUpVisual(buttonImageFileName)
				btn.SetOverVisual(buttonImageFileName)
				btn.SetDownVisual(buttonImageFileName)
				btn.Flash()
		# END_OF_QUEST_LETTER_IMAGE

		if localeInfo.IsARABIC():
			btn.SetToolTipText(name, 0, 35)
			btn.ToolTipText.SetHorizontalAlignCenter()
		else:
			btn.SetToolTipText(name, -20, 35)
			btn.ToolTipText.SetHorizontalAlignLeft()

		listOfTypes = iconType.split(",")
		if "blink" in listOfTypes:
			btn.Flash()

		listOfColors = {
			"golden":	0xFFffa200,
			"green":	0xFF00e600,
			"blue":		0xFF0099ff,
			"purple":	0xFFcc33ff,

			"fucsia":	0xFFcc0099,
			"aqua":		0xFF00ffff,
		}
		for k,v in listOfColors.iteritems():
			if k in listOfTypes:
				btn.ToolTipText.SetPackedFontColor(v)

		btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
		btn.Show()

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()

	def __ArrangeQuestButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		##!! 20061026.levites.퀘스트_위치_보정
		if self.wndParty.IsShow():
			xPos = 100 + 30
		else:
			xPos = 20

		if localeInfo.IsARABIC():
			xPos = xPos + 15

		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for btn in self.questButtonList:

			btn.SetPosition(xPos + (int(count/yCount) * 100), yPos + (count%yCount * 63))
			count += 1
			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				btn.Show()

	def __StartQuest(self, btn):
		event.QuestButtonClick(btn.index)
		self.__DestroyQuestButton(btn)

	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn

		return 0

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

	def HideAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Hide()

	def ShowAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Show()
	#####################################################################################

	#####################################################################################
	### Whisper ###

	def __InitWhisper(self):
		chat.InitWhisper(self)

	## 채팅창의 "메시지 보내기"를 눌렀을때 이름 없는 대화창을 여는 함수
	## 이름이 없기 때문에 기존의 WhisperDialogDict 와 별도로 관리된다.
	def OpenWhisperDialogWithoutTarget(self):
		if not self.dlgWhisperWithoutTarget:
			dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
			dlgWhisper.BindInterface(self)
			dlgWhisper.LoadDialog()
			dlgWhisper.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)
			dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
			dlgWhisper.Show()
			self.dlgWhisperWithoutTarget = dlgWhisper

			self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		else:
			self.dlgWhisperWithoutTarget.SetTop()
			self.dlgWhisperWithoutTarget.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)

	## 이름 없는 대화창에서 이름을 결정했을때 WhisperDialogDict에 창을 넣어주는 함수
	def RegisterTemporaryWhisperDialog(self, name):
		if not self.dlgWhisperWithoutTarget:
			return

		btn = self.__FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

		elif self.whisperDialogDict.has_key(name):
			oldDialog = self.whisperDialogDict[name]
			oldDialog.Destroy()
			del self.whisperDialogDict[name]

		self.whisperDialogDict[name] = self.dlgWhisperWithoutTarget
		self.dlgWhisperWithoutTarget.OpenWithTarget(name)
		self.dlgWhisperWithoutTarget = None
		self.__CheckGameMaster(name)

	## 캐릭터 메뉴의 1:1 대화 하기를 눌렀을때 이름을 가지고 바로 창을 여는 함수
	def OpenWhisperDialog(self, name):
		if not self.whisperDialogDict.has_key(name):
			dlg = self.__MakeWhisperDialog(name)
			dlg.OpenWithTarget(name)
			dlg.chatLine.SetFocus()
			dlg.Show()

			self.__CheckGameMaster(name)
			btn = self.__FindWhisperButton(name)
			if 0 != btn:
				self.__DestroyWhisperButton(btn)

	## 다른 캐릭터로부터 메세지를 받았을때 일단 버튼만 띄워 두는 함수
	def RecvWhisper(self, name):
		if not self.whisperDialogDict.has_key(name):
			btn = self.__FindWhisperButton(name)
			if 0 == btn:
				btn = self.__MakeWhisperButton(name)
				btn.Flash()
				app.FlashApplication()

				chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))

			else:
				btn.Flash()
				app.FlashApplication()
		elif self.IsGameMasterName(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def MakeWhisperButton(self, name):
		self.__MakeWhisperButton(name)

	## 버튼을 눌렀을때 창을 여는 함수
	def ShowWhisperDialog(self, btn):
		try:
			self.__MakeWhisperDialog(btn.name)
			dlgWhisper = self.whisperDialogDict[btn.name]
			dlgWhisper.OpenWithTarget(btn.name)
			dlgWhisper.Show()
			self.__CheckGameMaster(btn.name)
		except:
			import dbg
			dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")

		## 버튼 초기화
		self.__DestroyWhisperButton(btn)

	## WhisperDialog 창에서 최소화 명령을 수행했을때 호출되는 함수
	## 창을 최소화 합니다.
	def MinimizeWhisperDialog(self, name):

		if 0 != name:
			self.__MakeWhisperButton(name)

		self.CloseWhisperDialog(name)

	## WhisperDialog 창에서 닫기 명령을 수행했을때 호출되는 함수
	## 창을 지웁니다.
	def CloseWhisperDialog(self, name):

		if 0 == name:

			if self.dlgWhisperWithoutTarget:
				self.dlgWhisperWithoutTarget.Destroy()
				self.dlgWhisperWithoutTarget = None

			return

		try:
			dlgWhisper = self.whisperDialogDict[name]
			dlgWhisper.Destroy()
			del self.whisperDialogDict[name]
		except:
			import dbg
			dbg.TraceError("interface.CloseWhisperDialog - Failed to find key")

	## 버튼의 개수가 바뀌었을때 버튼을 재정렬 하는 함수
	def __ArrangeWhisperButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		xPos = screenWidth - 70
		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63
		#yCount = (screenHeight - 285) / 63

		count = 0
		for button in self.whisperButtonList:

			button.SetPosition(xPos + (int(count/yCount) * -50), yPos + (count%yCount * 63))
			count += 1

	## 이름으로 Whisper 버튼을 찾아 리턴해 주는 함수
	## 버튼은 딕셔너리로 하지 않는 것은 정렬 되어 버려 순서가 유지 되지 않으며
	## 이로 인해 ToolTip들이 다른 버튼들에 의해 가려지기 때문이다.
	def __FindWhisperButton(self, name):
		for button in self.whisperButtonList:
			if button.name == name:
				return button

		return 0

	## 창을 만듭니다.
	def __MakeWhisperDialog(self, name):
		dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
		dlgWhisper.BindInterface(self)
		dlgWhisper.LoadDialog()
		dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
		self.whisperDialogDict[name] = dlgWhisper

		self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		return dlgWhisper

	## 버튼을 만듭니다.
	def __MakeWhisperButton(self, name):
		whisperButton = uiWhisper.WhisperButton()
		if self.IsGameMasterName(name):
			whisperButton.SetUpVisual("d:/ymir work/ui/mail_gm_closed.tga")
			whisperButton.SetOverVisual("d:/ymir work/ui/mail_gm_open.tga")
			whisperButton.SetDownVisual("d:/ymir work/ui/mail_gm_open.tga")
			whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
		else:
			whisperButton.SetUpVisual("d:/ymir work/ui/mail_normal_closed.tga")
			whisperButton.SetOverVisual("d:/ymir work/ui/mail_normal_opend.tga")
			whisperButton.SetDownVisual("d:/ymir work/ui/mail_normal_opend.tga")
			whisperButton.SetToolTipText(name)
		whisperButton.ToolTipText.SetHorizontalAlignCenter()
		whisperButton.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), whisperButton)
		whisperButton.Show()
		whisperButton.name = name

		self.whisperButtonList.insert(0, whisperButton)
		self.__ArrangeWhisperButton()

		return whisperButton

	def __DestroyWhisperButton(self, button):
		button.SetEvent(0)
		self.whisperButtonList.remove(button)
		self.__ArrangeWhisperButton()

	def HideAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Hide()

	def ShowAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Show()

	def __CheckGameMaster(self, name):
		if not self.listGMName.has_key(name):
			return
		if self.whisperDialogDict.has_key(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def RegisterGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return
		self.listGMName[name] = "GM"

	def IsGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return True
		else:
			return False

	#####################################################################################

	#####################################################################################
	### Guild Building ###

	def BUILD_OpenWindow(self):
		self.wndGuildBuilding = uiGuild.BuildGuildBuildingWindow()
		self.wndGuildBuilding.Open()
		self.wndGuildBuilding.wnds = self.__HideWindows()
		self.wndGuildBuilding.SetCloseEvent(ui.__mem_func__(self.BUILD_CloseWindow))

	def BUILD_CloseWindow(self):
		self.__ShowWindows(self.wndGuildBuilding.wnds)
		self.wndGuildBuilding = None

	def BUILD_OnUpdate(self):
		if not self.wndGuildBuilding:
			return

		if self.wndGuildBuilding.IsPositioningMode():
			import background
			x, y, z = background.GetPickingPoint()
			self.wndGuildBuilding.SetBuildingPosition(x, y, z)

	def BUILD_OnMouseLeftButtonDown(self):
		if not self.wndGuildBuilding:
			return

		# GUILD_BUILDING
		if self.wndGuildBuilding.IsPositioningMode():
			self.wndGuildBuilding.SettleCurrentPosition()
			return True
		elif self.wndGuildBuilding.IsPreviewMode():
			pass
		else:
			return True
		# END_OF_GUILD_BUILDING
		return False

	def BUILD_OnMouseLeftButtonUp(self):
		if not self.wndGuildBuilding:
			return

		if not self.wndGuildBuilding.IsPreviewMode():
			return True

		return False

	def BULID_EnterGuildArea(self, areaID):
		# GUILD_BUILDING
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()

		if mainCharacterName != masterName:
			return

		if areaID != player.GetGuildID():
			return
		# END_OF_GUILD_BUILDING

		self.wndGameButton.ShowBuildButton()

	def BULID_ExitGuildArea(self, areaID):
		self.wndGameButton.HideBuildButton()
				
	if app.__BL_CHEST_DROP_INFO__:
		def OpenChestDropWindow(self, itemVnum, isMain):
			if self.wndChestDropInfo:
				self.wndChestDropInfo.Open(itemVnum, isMain)
	#####################################################################################

	def IsEditLineFocus(self):
		if self.ChatWindow.chatLine.IsFocus():
			return 1

		if self.ChatWindow.chatToLine.IsFocus():
			return 1

		return 0

	def EmptyFunction(self):
		pass

if __name__ == "__main__":

	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui
	import localeInfo

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(True)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create(localeInfo.APP_TITLE, systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()

	class TestGame(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)

			localeInfo.LoadLocaleData()
			player.SetItemData(0, 27001, 10)
			player.SetItemData(1, 27004, 10)

			self.interface = Interface()
			self.interface.MakeInterface()
			self.interface.ShowDefaultWindows()
			self.interface.RefreshInventory()
			#self.interface.OpenCubeWindow()

		def __del__(self):
			ui.Window.__del__(self)

		def OnUpdate(self):
			app.UpdateGame()

		def OnRender(self):
			app.RenderGame()
			grp.PopState()
			grp.SetInterfaceRenderState()

	game = TestGame()
	game.SetSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	game.Show()

	app.Loop()

	if app.ENABLE_DUNGEON_INFO_SYSTEM:
		def ShowDungeonInfoInterface(self):
			if app.ENABLE_PLAYER_SECURITY_SYSTEM and player.IsSecurityActivate():
				return
			if False == self.wndDungeonInfo.IsShow():
				self.wndDungeonInfo.Open()
			else:
				self.wndDungeonInfo.Close()
